import dbMgr
import traceback

class getCarsDTO():
    def __init__(self):
        self.dbmgr = dbMgr.dbMgr() 

    def get_urls(self):
        try:
            query = """select url from url_storage where url_active = 'Y';"""
            results = self.dbmgr.execute_query(query)
            return results
        except Exception as e:
            print(e) 

    def check_post_id(self, post_id):
        query = f"""select * from post_results where post_id = '{post_id}';"""
        results = self.dbmgr.execute_query(query)
        if results == '[]': 
            return True
        else: 
            return False 

    def post_results(self, post_time, post_id, post_link, post_price):
        try:
            query = f"""insert into post_results (post_id, post_link, post_price)
                        values ('{post_id}', '{post_link}', '{post_price}');"""
            self.dbmgr.insert_update(query)


        except Exception:
            traceback_message = traceback.format_exc()
            self.post_error(traceback_message)

    def post_error(self, traceback_message):
        traceback_message = traceback_message.replace("'", '"')
        query = f"""insert into error_log (error_contents) values('{traceback_message}')"""
        self.dbmgr.insert_update(query)
