from MongoConnection import MongoConnection


class Result():
    def __init__(self):
        self.db_object = MongoConnection("localhost", 27017, 'mcq')
        self.table_name = 'result'
        self.db_object.create_table(self.table_name, '_id')

    def save_result(self, result={}):
        self.db_object.update_upsert(self.table_name, result, result)

    def find_ioe_exam_rank(self, exam_code, useruid):
        aggregation_pipeline = []
        result = self.db_object.aggregrate_all(self.table_name, [
                {'$match': {'exam_code' : int(exam_code)}},
                { "$unwind": "$result" },
                { "$group": {
                 "_id": "$_id",
                 "result": { "$push": "$result" },
                 "useruid": { "$first": "$useruid" },
                 "exam_code": { "$first": "$exam_code" },
                 "ess_time": { "$first": "$ess_time" },
                 "Total": { 
                     "$max": {
                         "$cond": [
                             { "$eq": [ "$result.subject", "Total" ] },
                             "$result.score",
                             0
                         ]
                     }
                 },
                 "Physics": { 
                     "$max": {
                         "$cond": [
                             { "$eq": [ "$result.subject", "Physics" ] },
                             "$result.score",
                             0
                         ]
                     }
                 },
                 "Mathematics": { 
                     "$max": {
                         "$cond": [
                             { "$eq": [ "$result.subject", "Mathematics" ] },
                             "$result.score",
                             0
                         ]
                     }
                 },
                 "Chemistry": { 
                     "$max": {
                         "$cond": [
                             { "$eq": [ "$result.subject", "Chemistry" ] },
                             "$result.score",
                             0
                         ]
                     }
                 },
                 "English": { 
                     "$max": {
                         "$cond": [
                             { "$eq": [ "$result.subject", "Biology" ] },
                             "$result.score",
                             0
                         ]
                     }
                 },
                 "Aptitude": { 
                     "$max": {
                         "$cond": [
                             { "$eq": [ "$result.subject", "Biology" ] },
                             "$result.score",
                             0
                         ]
                     }
                 }
             }},

             
             { "$sort": {
                 "Total": -1,
                 "Physics": -1,
                 "Mathematics": -1,
                 "Chemistry": -1,
                 "English": -1,
                 "Aptitude": -1,
             }},

             
             { "$project": {
                 "result": 1,
                 "useruid": 1,
                 "exam_code": 1,
                 "ess_time": 1
             }}
        ])
        # rank = next(index for (index, d) in enumerate(result) if d["useruid"] == useruid)
        return result
