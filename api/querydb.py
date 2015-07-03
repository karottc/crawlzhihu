#coding=UTF-8
__author__ = 'karottc'

import MySQLdb
import json
import logging
import time

__metaclass__=type

class QueryDB:
    def __init__(self):
        self.db = MySQLdb.connect("localhost","root","","zhihu", use_unicode=True, charset="utf8")
        self.cursor = self.db.cursor()
        self.indexNum = 10
        now = time.time()
        year, mon, day, hour, minutes, val, val, val, val = time.localtime(now)
        logPath = '/root/testproject/mysite/log/zhihu_%d%02d%02d.log' % (year, mon, day)
        logPath = 'zhihu_%d%02d%02d.log' % (year, mon, day)
        logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(funcName)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename=logPath,
                filemode='a')

    def __del__(self):
        self.db.close()
        logging.shutdown()

    def QueryIndex(self, timestamp=0):
        if 0 == timestamp:
            sql = 'select fstoryid,ftitlename,fnum, frecomm, ftitlepic, ftitlebigpic, fdisplaydate, fupdatetime from \
                   t_zhihu_daily_index ORDER BY fupdatetime DESC LIMIT %d' % self.indexNum
        else:
            sql = 'select fstoryid,ftitlename,fnum, frecomm, ftitlepic, ftitlebigpic, fdisplaydate, fupdatetime from t_zhihu_daily_index \
               WHERE fupdatetime<%d ORDER BY fupdatetime DESC LIMIT %d' % (timestamp, self.indexNum)

        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            listRet = []

            for row in results:
                dictStory = {}
                dictStory['id'] = row[0]
                dictStory['images'] = row[4]
                dictStory['title'] = row[1]
                dictStory['display_date'] = row[6]
                dictStory['timestamp'] = row[7]
                listRet.append(dictStory)
            logging.info(listRet)
            return listRet
        except Exception, e:
            logging.error(e)
            return []

    def QueryStory(self, id):
        sql = 'select fstoryid, ftitle, fnum, fanwser, fviewmore from t_zhihu_daily_story where fstoryid=%d ORDER BY fid' % id
        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            listRet = []

            for row in results:
                dictStory = {}
                dictStory['question_title'] = row[1]
                dictStory['answer_num'] = row[2]
                strTemp = row[3]
                # 这个是为了处理{"answer": "<img src="http://pic4.zhimg.com/49c977e6c68beccfe8f594258b397067_b.jpg" 这种情况
                # 这种会和json的属性双引号冲突
                pos = strTemp.find('img src')
                if pos != -1:
                    str1 = strTemp[0:pos]
                    str2 = strTemp[pos:]
                    endPos = str2.find('>')
                    str3 = str2[0:endPos]    # 这一段是<img src.....>
                    str4 = str2[endPos:]
                    str3 = str3.replace('"', "'")
                    strTemp = str1 + str3 + str4
                dictStory['answers'] = json.loads(strTemp, strict=False)
                #dictStory['answer'] = row[3]
                dictStory['viewmore'] = row[4]
                listRet.append(dictStory)
            logging.info(listRet)
            return listRet
        except Exception, e:
            logging.error(e)
            return []

#gt = QueryDB()
#print gt.QueryStory(4840691)
