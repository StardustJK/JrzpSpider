from elasticsearch_dsl import Document, Keyword, Text,Float,Integer,Date
from elasticsearch_dsl.connections import connections
es=connections.create_connection(hosts=["http://elastic:123456@10.112.134.244:9200"])

class JrzpType(Document):
    class Index:
        name = "jrzp"
        settings = {
            "number_of_shards": 1,
            "number_of_replicas": 0,
        }
        mappings = {
            "properties": {
                "pos_name": {
                    "type": "text"
                },
                "salary_low_bound": {
                    "type": "float"
                },
                "salary_high_bound": {
                    "type": "float"
                },
                "salary_fee_months": {
                    "type": "integer"
                },
                "pos_keyword": {
                    "type": "text"
                },
                "pos_domain": {
                    "type": "keyword"
                },
                "city": {
                    "type": "keyword"
                },
                "location": {
                    "type": "text"
                },
                "degree": {
                    "type": "keyword"
                },
                "exp": {
                    "type": "keyword"
                },
                "person_in_charge": {
                    "type": "text"
                },
                "charge_pos": {
                    "type": "text"
                },
                "pos_detail": {
                    "type": "text"
                },
                "enterprise": {
                    "type": "text"
                },
                "enterprise_scale": {
                    "type": "keyword"
                },
                # 新增字段：用于根据企业规模进行排序
                "scale_mapping": {
                    "type": "integer"
                },
                "create_time": {
                    "type": "date",
                    "format": "yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||epoch_millis"
                },
                "url": {
                    "type": "text"
                },
                "pos_source": {
                    "type": "text"
                }
            }
        }
    pos_name = Text(analyzer="ik_smart")
    salary_low_bound = Float()
    salary_high_bound = Float()
    salary_fee_months = Integer()

    pos_keyword = Text(analyzer="ik_smart")
    pos_domain = Keyword()

    city = Keyword()
    location = Text(analyzer="ik_smart")

    degree = Keyword()
    exp = Keyword()

    person_in_charge = Text(analyzer="ik_smart")
    charge_pos = Text(analyzer="ik_smart")

    pos_detail = Text(analyzer="ik_smart")

    enterprise = Text(analyzer="ik_smart")
    enterprise_scale = Keyword()
    create_time = Date()
    url = Text()
    pos_source = Text(analyzer="ik_smart")

    def __init__(self, item):
        super(JrzpType, self).__init__()
        self.assignment(item)

    # 将item转换为es的数据
    def assignment(self, item):
        keys = ['pos_name',
                'salary_low_bound',
                'salary_high_bound',
                'salary_fee_months',
                'pos_keyword',
                'pos_domain',
                'city',
                'location',
                'degree',
                'exp',
                'person_in_charge',
                'charge_pos',
                'pos_detail',
                'enterprise',
                'enterprise_scale',
                'create_time',
                'url',
                'pos_source'
                ]
        for key in keys:
            try:
                item[key]
            except:
                item[key] = ''
        # 将字段值转换为es的数据
        # 虽然只是将原来的item值赋给了成员变量，但这个过程中会执行数据格式转换操作，
        # 比如url本来在item是python的字符串类型，转换后变为es的keyword类型
        self.pos_name = item['pos_name']
        self.salary_low_bound = item['salary_low_bound']
        self.salary_high_bound = item['salary_high_bound']
        self.salary_fee_months = item['salary_fee_months']
        self.pos_keyword = item['pos_keyword']
        self.pos_domain = item['pos_domain']
        self.city = item['city']
        self.location = item['location']
        self.degree = item['degree']
        self.exp = item['exp']
        self.person_in_charge = item['person_in_charge']
        self.charge_pos = item['charge_pos']
        self.pos_detail = item['pos_detail']
        self.enterprise = item['enterprise']
        self.enterprise_scale = item['enterprise_scale']
        self.create_time = item['create_time']
        self.url = item['url']
        self.pos_source = item['pos_source']