db.result.aggregate([
     {'$match': {'exam_code' : 391}},
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


 { "$group": {
                 "_id": "roshan",
                 "count":{"$sum":1},
                 "results:"{"$push":{}}
                 }
                 },
     
     { "$project": {
         "result": 1,
         "useruid": 1,
         "exam_code": 1,
         "ess_time": 1
     }}
])