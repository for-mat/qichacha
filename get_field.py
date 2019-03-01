# -*- coding: utf-8 -*-
"""
获取网页字段信息
"""



def get_fields(self ,unique ,token ,proxy ,headers):
    # 获取网页，取出json中的公司信息
    # 设置代理ip
    self.proxy = proxy
    self.headers = headers_pool.requests_headers()
    # print headers
    js = requests.get('https://xcx.qichacha.com/wxa/v1/base/getMoreEntInfo?unique=%s&token=%s' % (unique ,token), headers = headers, proxies=self.proxy ,verify=False, timeout=1)
    # print js.cookies
    js = js.text
    print js
    js = json.loads(js)
    result = js.get('result')
    self.result = result
    # company = result.get('Company')

    # 获取字段
    self.name = result.get('Name')
    self.phone = result.get('ContactInfo').get('PhoneNumber')

    try:
        self.website = result.get('ContactInfo').get('WebSite')[0].get('Url')
    except TypeError:
        self.website = None

    self.email = result.get('ContactInfo').get('Email')
    self.province = result.get('Area').get('Province')
    self.city = result.get('Area').get('City')
    self.county = result.get('Area').get('County')
    self.address = result.get('Address')

    reg = re.compile('<[^>]*>')
    intro = result.get('ProfileDesc')
    self.intro = reg.sub('' ,intro).strip()

    self.registered_capital = result.get('RegistCapi')
    self.actual_capital = result.get('RecCap')
    self.operating_state = result.get('Status')
    self.establishment_date = result.get('StartDate')
    self.uscc = result.get('CreditCode')
    self.taxpayer_number = result.get('TaxNo')
    self.registration_number = result.get('No')
    self.organization_code = result.get('OrgNo')
    self.type = result.get('EconKind')
    self.industry = result.get('Industry').get('Industry')

    approval_date = result.get('CheckDate')
    if approval_date < 0:
        approval_date = 0
    approval_date = time.localtime(approval_date)
    self.approval_date = time.strftime("%Y-%m-%d" ,approval_date)

    self.registration_authority = result.get('BelongOrg')
    self.area = result.get('Area').get('Province')
    self.english_name =result.get('EnglishName')

    used_name_list = result.get('OriginalName')
    used_name = ""
    if type(used_name_list) == list:
        for i in used_name_list:
            used_name = used_name + (i.get('Name')) + " "
            self.used_name = used_name
    else:
        self.used_name = None

    try:
        self.insurancer_count = result.get('CommonList')[3].get('Value')
    except:
        self.insurancer_count = None

    self.staff_count = result.get('profile').get('Info')

    StartDate = result.get('StartDate')
    StartDate = str(StartDate)
    EndDate = result.get('EndDate')
    EndDate = str(EndDate)
    if EndDate == '0':
        EndDate = 'Indefinite'
    self.operation_period = StartDate + ' unitl ' + EndDate

    self.operation_scope = result.get('Scope')

    name = json.dumps(self.name, encoding="utf-8", ensure_ascii=False)
    phone = json.dumps(self.phone, encoding="utf-8", ensure_ascii=False)
    website = json.dumps(self.website, encoding="utf-8", ensure_ascii=False)
    email = json.dumps(self.email, encoding="utf-8", ensure_ascii=False)
    province = json.dumps(self.province, encoding="utf-8", ensure_ascii=False)
    city = json.dumps(self.city, encoding="utf-8", ensure_ascii=False)
    county = json.dumps(self.county, encoding="utf-8", ensure_ascii=False)
    address = json.dumps(self.address, encoding="utf-8", ensure_ascii=False)
    intro = json.dumps(self.intro, encoding="utf-8", ensure_ascii=False)
    registered_capital = json.dumps(self.registered_capital, encoding="utf-8", ensure_ascii=False)
    actual_capital = json.dumps(self.actual_capital, encoding="utf-8", ensure_ascii=False)
    operating_state = json.dumps(self.operating_state, encoding="utf-8", ensure_ascii=False)
    establishment_date = json.dumps(self.establishment_date, encoding="utf-8", ensure_ascii=False)
    uscc = json.dumps(self.uscc, encoding="utf-8", ensure_ascii=False)
    taxpayer_number = json.dumps(self.taxpayer_number, encoding="utf-8", ensure_ascii=False)
    registration_number = json.dumps(self.registration_number, encoding="utf-8", ensure_ascii=False)
    organization_code = json.dumps(self.organization_code, encoding="utf-8", ensure_ascii=False)
    type1 = json.dumps(self.type, encoding="utf-8", ensure_ascii=False)
    industry = json.dumps(self.industry, encoding="utf-8", ensure_ascii=False)
    approval_date = json.dumps(self.approval_date, encoding="utf-8", ensure_ascii=False)
    registration_authority = json.dumps(self.registration_authority, encoding="utf-8", ensure_ascii=False)
    area = json.dumps(self.area, encoding="utf-8", ensure_ascii=False)
    english_name = json.dumps(self.english_name, encoding="utf-8", ensure_ascii=False)
    used_name = json.dumps(self.used_name, encoding="utf-8", ensure_ascii=False)
    insurancer_count = json.dumps(self.insurancer_count, encoding="utf-8", ensure_ascii=False)
    staff_count = json.dumps(self.staff_count, encoding="utf-8", ensure_ascii=False)
    operation_period = json.dumps(self.operation_period, encoding="utf-8", ensure_ascii=False)
    operation_scope = json.dumps(self.operation_scope, encoding="utf-8", ensure_ascii=False)

    fields = (name, phone, website, email, province, city, county, address, intro, registered_capital, actual_capital,
              operating_state, establishment_date, uscc, taxpayer_number, registration_number, organization_code, type1,
              industry, approval_date, registration_authority, area, english_name, used_name, insurancer_count,
              staff_count, operation_period, operation_scope)
    return fields, result
