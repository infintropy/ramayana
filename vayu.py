
import airtable
import json
import base64
import os

'''
#
###
#######
##############
#################################
#################################
 __     ___ __   ___   _    #####
 \ \   / / \\ \ / / | | |   #######
  \ \ / / _ \\ V /| | | |   ###########
   \ V / ___ \| | | |_| |   ###################
    \_/_/   \_\_|  \___/                 ######
                                         ######
- Airtable connection module for BRAHMA. ######
- Used with the <name> caching module.   ######
                                         ######  
###############################################
###############################################
############## 
#######
###
#                   



Vayu is a communication module for AirTable connecting with Brahma entities. 

Ideas:
    Will probably need to configure a simpler artist paradigm, (not officially USER based (with credentialing)) so that people can just use the front end 
    For this, would be easy to keep the login front-end within Brahma and then register account information as info on a specific base. 
        - This way, a site only has to maintain $20 a momth record keeping, and exploit having multiple users accessing 50,000 records/base



'''





API_KEY = 'keyyeOyrgbQQ9qvLh'
CONFIG_BASE_KEY = 'appZS0IqdlNPJszXv'
os.environ['AIRTABLE_API_KEY'] = API_KEY

REALIGN = 'appJLatmhJPKftvrd'





        
    
    


class SessionManager():
    '''
    It is assumed that entities are limited to the preconfigured tables. 
    
    We must 
        1) Define the sessions: storing the key for the project and its tables.
        2) Define if a project has a default configuration, or if it has entities that can be extended. 
           Extending and integrating new entities is quite easy as long as you register them. 
           For speed and unlike Shotgun, you can define custom entities at will and not have to enable them site wide. 
    '''


    def __init__(self):
        '''
        store session information in a configuration table, retrieve that information and then build a session dict which we will wrap and use to call different projects
        '''
        self.session_mapping = None
        self.base = {}
        self.table = {}
        self.default_entities = None
        #builds the session obj
        self.config = {}
        for s in ['MASTER', 'DEFAULT_ENTITIES']:
            self.config[s] = airtable.Airtable( CONFIG_BASE_KEY, s)
        self.get_sessions()
        
    def get_sessions(self, all=None):
        opt = ['active']
        if all:
            opt.append('archived')
        session_mapping = self.config['MASTER'].get_all(fields=['project_code', 'session_id'], formula="{status}='active'")
        self.session_mapping = dict((i['fields']['project_code'], i['fields']['session_id'])  for i in session_mapping)
        return self.session_mapping
    
    def get_project_entities(self):
        pass
    
    def build_all_sessions(self):
        '''
        This is the main session object.
        '''

        entities = self.default_project_entities()

        if self.session_mapping:
            for k,v in self.session_mapping.iteritems():
                if k in self.base.keys():
                    print "INFO:: ALREADY FOUND:: {}:: SKIPPING".format( k )  
                    pass
                else:
                
                    self.base[k] = {}
                    for e in entities:
                        if e in self.base[k].keys():
                            print "INFO:: ALREADY FOUND:: {} >> TABLE:: {} into main session object.".format( k, e )  
                            
                        else:
                            try:
                                self.base[k][e] = airtable.Airtable(v, e)
                                print "INFO:: MAPPED BASE:: {} >> TABLE:: {} into main session object.".format( k, e )  
                            except:
                                print "ERROR:: Couldnt establish base {}:{}".format(k, e)
                        
    

    def default_project_entities(self):
        '''
        These are the default entities that each project will contain. 
        If you would like to add more entities, make 
        '''
        default_entities =  self.config['DEFAULT_ENTITIES'].get_all(fields="Entity")
        self.default_entities = [i['fields']['Entity'] for i in default_entities]
        return self.default_entities
    
    def remove_session(self, name):
        if name in self.session_mapping.keys():
            self.base.pop(name)
            
    def build_entity_sessions(self):
        pass
    
            
  
    def find(self, entity_name, fields=None, formula=None, project=None, view=None, id=None):
        res = []
        keys = self.base.keys()
        if project:
            keys = [project]
        for b in keys:
            if id:
                formula="RECORD_ID='{}'".format(id)
            if fields:
                res.extend( self.base[b][entity_name].get_all( fields=fields, formula=formula, view=view) )
            else:
                res.extend( self.base[b][entity_name].get_all(  formula=formula ) )
        return res
        
        
    def find_one(self, entity_name, fields=None, formula=None, project=None, view=None):
        return self.find(entity_name, fields=fields, formula=formula, project=project, view=view)[0]
    
    def update(self, entity_name, where=None, id=None, fields=None, project=None):
        record = {}
        if where and type(where)==dict:
            records = self.find_one(entity_name, formula="{{{field}}}='{value}'".format(field=where.items()[0][0], value=where.items()[0][1] ))
            record['id'] = records['id']
        else:
            if id:
                record['id'] = id
            else:
                raise ValueError("Need to supply an ID to update.")
        if not fields:
            raise ValueError("Need to supply a dict describing column/values to update")
        else:
            if project and project in self.base.keys():
                print 'populating proper project'
                print project
                print id
                try:
                    return self.base[project][entity_name].update(id, fields=fields)
                except:
                    pass
            else:
                for b in self.base.keys():
                    try:
                        self.base[b][entity_name].update(id, fields=fields)
                    except:
                        pass
                
        
            
class CacheWrap():

    pass

