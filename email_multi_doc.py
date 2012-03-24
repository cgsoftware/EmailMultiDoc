# -*- encoding: utf-8 -*-




import pooler
import tools

from tools.translate import _
from osv import fields,osv
import time
import netsvc
from tools.misc import UpdateableStr, UpdateableDict

class email_multi_doc(osv.osv_memory):
 _name = 'email.multi_doc'
 _description = 'Genera Invia Email per i Doc Selezionati '
 _columns = {
            'subject':fields.char('Oggetto ',  size=64, required=True),
            'text': fields.text('Testo Messagio', required=True),
            }    

 
 
 def default_get(self, cr, uid, fields, context=None):
        data={}
        p = pooler.get_pool(cr.dbname)
        user = p.get('res.users').browse(cr, uid, uid, context)
        pool = pooler.get_pool(cr.dbname)
        fatture = pool.get('fiscaldoc.header')
        active_ids = context and context.get('active_ids', [])
        if not active_ids:
            raise osv.except_osv(_('Warning'), _('Devi Selezionare almeno un Documento'))
        subject = "Documento MainettiOmaf "
        text = """ In Allegato Nostri Documenti """
        user = p.get('res.users').browse(cr, uid, uid, context)
        text = text + '\n--\n' + user.signature                
        return {'subject': subject, 'text': text}


 def  get_data(self, cr, uid, active_ids, context=None):
        #import pdb;pdb.set_trace()
        #pool = pooler.get_pool(cr.dbname)
        fatture =self.pool.get('fiscaldoc.header')
        Primo = True
        if active_ids:
            for doc in fatture.browse(cr, uid, active_ids, context=context):
                if Primo:
                    Primo = False
                    DtIni = doc['data_documento']
                    NrIni = doc['name']
                    danr = doc['id']
                  #import pdb;pdb.set_trace()
                DtFin = doc['data_documento']
                NrFin = doc['name']
                anr = doc['id']
        return{'dadata':DtIni,'adata':DtFin,'danrv':NrIni,'anrv':NrFin,'sconto':False,'prezzi':False, 'agente':0}

 def _build_contexts(self, cr, uid, ids, data, context=None):
        #import pdb;pdb.set_trace()
        if context is None:
            context = {}
        result = {}
        sub = data['form']['danrv']
        result = {'danr':data['form']['danrv'],'anr':data['form']['anrv'],'dadata':data['form']['dadata'],
                  'adata':data['form']['adata'], 'sconto':data['form']['sconto'], 'prezzi':data['form']['prezzi'], 'name':sub}
        var = data['form']['prezzi']
        #import pdb;pdb.set_trace()
        if var is True or 1:
            result = {'danr':data['form']['danrv'],'anr':data['form']['anrv'],'dadata':data['form']['dadata'],
                  'adata':data['form']['adata'], 'sconto':data['form']['sconto'], 'prezzi':1,'name':sub}
        else:
            result = {'danr':data['form']['danrv'],'anr':data['form']['anrv'],'dadata':data['form']['dadata'],
                  'adata':data['form']['adata'], 'sconto':data['form']['sconto'], 'prezzi':0,'name':sub}
        return result

 def create_report(self,cr, uid, res_ids, report_name=False, file_name=False,data=False,context=False):
        #import pdb;pdb.set_trace()
        if not report_name or not res_ids:
            return (False, Exception('Report name and Resources ids are required !!!'))
        try:
            ret_file_name = file_name
            service = netsvc.LocalService("report."+report_name);
            (result, format) = service.create(cr, uid, res_ids, data, context)
            fp = open(ret_file_name, 'wb+');
            fp.write(result);
            fp.close();
        except Exception,e:
            print 'Exception in create report:',e
            return (False, str(e))
        return (True, ret_file_name)


 def report_name(self, cr, uid, ids, data, context=None):
        #import pdb;pdb.set_trace()
        if context is None:
            context = {}
        pool = pooler.get_pool(cr.dbname)
        fatture = pool.get('fiscaldoc.header')
        active_ids = context and context.get('active_ids', [])
        Primo = True
        if active_ids:
            for doc in fatture.browse(cr, uid, active_ids, context=context):
                if Primo:
                    Primo = False
                    IdTipoSta = doc.tipo_doc.id
                    TipoStampa = doc.tipo_doc.tipo_modulo_stampa.report_name
                #import pdb;pdb.set_trace()
                else:
                  if IdTipoSta <> doc.tipo_doc.id:
                      raise osv.except_osv(_('ERRORE !'),_('Devi Selezionare documenti con la stessa Causale Documento'))

        return TipoStampa #{



 def genera(self, cr, uid, ids, context):
      p = pooler.get_pool(cr.dbname)
      account_smtpserver_id = p.get('email.smtpclient').search(cr, uid, [('type','=','account'),('state','=','confirm'),('active','=',True)], context=False)
      if not account_smtpserver_id:
                  default_smtpserver_id = p.get('email.smtpclient').search(cr, uid, [('type','=','default'),('state','=','confirm'),('active','=',True)], context=False)
      smtpserver_id = account_smtpserver_id or default_smtpserver_id
      if smtpserver_id:
                smtpserver_id = smtpserver_id[0]
      else:
                raise osv.except_osv(_('Error'), _('Non Hai un Server SMTP definito!'))
    
      emails = 0
      docs = 0
      dati_email = self.browse(cr,uid,ids)[0]
      active_ids = context and context.get('active_ids', [])
      #import pdb;pdb.set_trace()
      fatture = self.pool.get('fiscaldoc.header').browse(cr,uid,active_ids)
      for fat in fatture: # cicla sui documenti
          #prepara e crea la stampa
          if context is None:
              context = {}
          data = {}
          data['ids'] = context.get('active_ids', [])
          data['model'] = context.get('active_model', 'ir.ui.menu')
          data['form'] = self.get_data(cr, uid, [fat.id],context)
          used_context = self._build_contexts(cr, uid, ids, data, context=context)
          data['form']['parameters'] = used_context
          to=[]
          # costruisce, la destinazione se vuota  allora va nella cartella dei documenti          
          for addr in fat.partner_id.address:
             if addr.email:
                 name = addr.name or addr.partner_id.name
                 to.extend(['%s <%s>' % (name, email) for email in addr.email.split(',')])
          if len(to)==0:
              # deve salvare il file nella cartella documenti
              file_name = fat.name.replace(' ','_')
              ret_file_name = '/home/openerp/documenti/'+file_name+'.pdf'
              report = self.create_report(cr, uid, data['ids'], self.report_name(cr, uid, [fat.id], data, context), ret_file_name,data,context)
              attachments = report[0] and [report[1]] or []
              docs +=1
          else:   
              # crea l'email     
              file_name = fat.name.replace(' ','_')
              ret_file_name = '/tmp/'+file_name+'.pdf'
              report = self.create_report(cr, uid, data['ids'], self.report_name(cr, uid, [fat.id], data, context), ret_file_name,data,context)
              attachments = report[0] and [report[1]] or []
              
              for email in to:
                  #print email, data['form']['subject'], data['ids'], data['form']['text'], data['model'], file_name
                  state = p.get('email.smtpclient').send_email(cr, uid, smtpserver_id, email, dati_email.subject, dati_email.text, attachments)
                  if not state:
                      raise osv.except_osv(_('Error sending email'), _('Please check the Server Configuration!'))
                  emails +=1
      #import pdb;pdb.set_trace()    
      ids_repo = self.pool.get('chiudi_invio').create(cr,uid,{'emails':emails,'docs':docs})
      context.update({'ids_repo':[ids_repo]})  
      return {
            'name': 'Report',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'chiudi_invio',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': context
            }



email_multi_doc()

class  chiudi_invio(osv.osv_memory):
    _name = 'chiudi_invio'
    _description = 'Report Invio Email per i Doc Selezionati '
    _columns = {
                'emails':fields.integer('Emails Inviate'),
                'docs':fields.integer('Documenti Salvati'),
                }
    def default_get(self, cr, uid, fields, context=None):
        ids = context.get('ids_repo',False)
        if ids:
            record = self.browse(cr,uid,ids)[0]    
            emails = record.emails
            docs = record.docs
        else:
            emails = 0
            docs = 0
        return {'emails': emails, 'docs': docs}
chiudi_invio()