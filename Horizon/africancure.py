''' african currencies
Algerian dinar=DZD,
 West African CFA franc=XOF
 Central African CFA franc =XAF
Congolese franc= CDF
Egyptian pound =EGP
Ghanaian cedi = GHS
Nigerian naira = NGN
Rwandan franc = RWF
Sierra Leonean leone = SLL
Somali shilling = SOS
South African rand = ZAR'''

#importing data for conversion
#https://free.currconv.com/api/v7/convert?q=GHS_RWF,GHS_DZD,GHS_XOF,GHS_XAF,GHS_CDF,GHS_EGP,GHS_NGN,GHS_SLL,GHS_ZAR&compact=ultra&apiKey=pr_1e39105e626d4d3f8722b0e4d888e891
#https://free.currconv.com/api/v7/convert?q=GHS_RWF,GHS_DZD,GHS_XOF,GHS_XAF,GHS_CDF,GHS_EGP,GHS_NGN,GHS_SLL,GHS_ZAR&compact=ultra&apiKey=b2c411fd35cfb042cc10
#https://prepaid.currconv.com/api/v7/convert?q=GHS_RWF,GHS_DZD,GHS_NGN,GHS_SLL&compact=ultra&=pr_apiKey1e39105e626d4d3f8722b0e4d888e891
def currency_data():
    import requests
    url = 'https://free.currconv.com/api/v7/convert?q=GHS_DZD&compact=ultra&apiKey=b2c411fd35cfb042cc10'
    response = requests.get(url)
    data = (response.json())
    data = str(data)
    import ast
    conversions = ast.literal_eval(data)
    globals().update(conversions)
    return (conversions)

    #converting from ghs
def currency_conversion(req_currency):
    #African_currency = {'GHS_DZD': DZD}
    #'XOF':GHS_XOF,'XAF': GHS_XAF, 'CDF':GHS_CDF, 'EGP':GHS_EGP, 'NGN': GHS_NGN, 'RWF':GHS_RWF, 'SLL':GHS_SLL, 'ZAR':GHS_ZAR}
    #globals().update(African_currency)
    req_currency = str(req_currency)
    #print (req_currency)
    conversion = int(input())
    #print(conversion)
    exchange = ((globals()[req_currency])*conversion)
    #print(exchange)
    exchange = str(exchange)
    return exchange
    #print("This will convert to " + exchange + " " + (req_currency) )


