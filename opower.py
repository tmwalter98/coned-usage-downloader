import requests

url = "https://cned.opower.com/ei/edge/apis/DataBrowser-v1/cws/utilities/cned/utilityAccounts/6669a4e4-14cd-11ed-ad4a-0200170a92cd/reads"

payload = {}
headers = {
    'Authorization': 'Bearer eyJraWQiOiJGbWlzN1NQbVpCcUVIaE1sUkxYRlU2cENwdFp4X2NIUHBYakMyTHQzdlRvIiwiYWxnIjoiUlMyNTYifQ.eyJ2ZXIiOjEsImp0aSI6IkFULmJnaVBOa0NOOGtqdlJCZ2RvNUVsSkFlcFhHb3lfcjE1VWx3Sl8zZl8yMUkub2FyMTIyMDMwcHNndXpLeFcweDciLCJpc3MiOiJodHRwczovL2NvbmVkLm9rdGEuY29tL29hdXRoMi9hdXNkc2tpdnNocmFTMTNkNjB4NyIsImF1ZCI6Imh0dHBzOi8vYXBpLmNvbmVkLmNvbSIsImlhdCI6MTY3MjQ0ODgwNywiZXhwIjoxNjcyNDUwNjA3LCJjaWQiOiJLVVFlcE5XbFdLUWxPYWtCVTVvMyIsInVpZCI6IjAwdXZ5ajB3ZnJjbm1zcGV3MHg3Iiwic2NwIjpbImRjeC5yZWFkX3Byb2ZpbGVfYWNjb3VudHMiLCJvZmZsaW5lX2FjY2VzcyJdLCJhdXRoX3RpbWUiOjE2NzI0NDc2MjAsInN1YiI6InRtd2FsdGVyOThAZ21haWwuY29tIn0.i4hhLBDvzXZFDp_ss4mirIzV_7Qswp8ywWY93976OPdvKja1f4cFbd_5Chc8XJxAwusuUPhTALYTG9PVHJks2UY0nzA0pTT_lk35jaMRLShPQhhMLA1P8JwKv6bao0POclH4X2VdSR3Y-F9GuQjKOf6SrcmM_DWvIaoY44leKoRBOgzePhZ5-aCdPGkWITO1nEkm5C4KT8Iy2LSLACiSymUcB2_oaMuLcQIXT43chiyxRtUJHYYTzGegaIn-rWZSUaJkNwYB-G54q6MpRK2tVShYWGjQFe2Ub9yK6c5Kw2P7D9wpxG5LPfFDwL-u6LI18_T6EhAJvgard96H81f6YQ',
    'Host': 'cned.opower.com',
    'Cookie': 'TS019baf05=01387d871f425435e7cf5354daa8c0132fce32d54745761ce68855718b6cde46336a9ad43135389c17309098fe13d87037f1bbb832'
}


response = requests.get(url=url,
                        headers=headers,
                        params={
                            'startDate': '2022-11-02',
                            'endDate': '2022-12-01',
                            'aggregateType': 'quarter_hour',
                            'includeEnhancedBilling': 'false',
                            'includeMultiRegisterData': 'false',
                        },
                        )

print(response.text)
