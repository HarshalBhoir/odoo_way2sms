
##################################    way2sms PYTHON   ###########################################

from odoo import models, fields, api, _
from odoo.exceptions import Warning
import datetime
from datetime import datetime
from dateutil.relativedelta import relativedelta
import re

import urllib2
import cookielib
from getpass import getpass
import sys
import os
from stat import *

class way2smsBase(models.Model):
    _name = "way.base"
    _rec_name = "user_name"
    
    user_name = fields.Char(string="UserName", required=True)
    password = fields.Char(string="Password", required=True)
    
class way2sms(models.Model):
    _name = "way.way"
    
    message = fields.Text(String="Message", size=140)
    number = fields.Text(string="Receiver Number", required= True, size=12)
    user_acc = fields.Many2one("way.base",'ACC', required= True)
    date_time = fields.Datetime(string="Date & Time",  readonly=True)
    
    

    def sendSms(self):
        url ='http://site24.way2sms.com/Login1.action?'
        data = 'username='+self.user_acc.user_name+'&password='+self.user_acc.password+'&Submit=Sign+in'
        cj= cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        opener.addheaders=[('User-Agent','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120')]
        try:
            usock =opener.open(url, data)
        except IOError:
            raise Warning(_("Error pls Check account or mobile number"))
        jession_id =str(cj).split('~')[1].split(' ')[0]
        send_sms_url = 'http://site24.way2sms.com/smstoss.action?'
        send_sms_data = 'ssaction=ss&Token='+jession_id+'&mobile='+self.number+'&message='+self.message+'&msgLen=136'
        opener.addheaders=[('Referer', 'http://site25.way2sms.com/sendSMS?Token='+jession_id)]
        try:
            sms_sent_page = opener.open(send_sms_url,send_sms_data)
        except IOError:
            raise Warning(_("Error pls Check account or mobile number"))
        self.date_time = str(datetime.now())
        raise Warning(_("Message Sent"))

    @api.one
    @api.constrains('number')
    def validatePhonenumber(self):
        for phone in self:
            if re.match("[0-9]", phone.number) == None:
                raise Warning("Mobile number is not valid one, Please specify valid number")
                return False
            return True
