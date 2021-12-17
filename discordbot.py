import discord
import re
import aiohttp
import asyncio
import json

global store

users = {'will': ['eyJraWQiOiJzMSIsInR5cCI6ImF0K2p3dCIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiI2NjYwYzc5MS05MGViLTU5ZDAtYjYyZS03MmE4OGU4YjVmODEiLCJzY3AiOlsib3BlbmlkIl0sImNsbSI6WyJvcGVuaWQiXSwiZGF0Ijp7ImxpZCI6IktwQy1nOEw5VzZEMnNKUXZzSVdROFEiLCJjIjoiZWMxIn0sImlzcyI6Imh0dHBzOlwvXC9hdXRoLnJpb3RnYW1lcy5jb20iLCJleHAiOjE2Mzk0MzUzMzUsImlhdCI6MTYzOTQzMTczNSwianRpIjoiQUdaSTRCZU9DMkUiLCJjaWQiOiJwbGF5LXZhbG9yYW50LXdlYi1wcm9kIn0.Xb2mLtWLFDOt4iqY9qDN7gutwqtWlng0YCiAoYMfpP1j2jelALsdKqfmz_fwpU7gvrqh2wEnVt9nI4yjyQd1522qAVIqSKF-q8_s94cdWb81o4QJwUrCrk84gFYdk9vfrRz02HDaot2yG4HkuqfNRyFtAK92YWCO4Y6VhXRd_3I',
                  'eyJraWQiOiJrMSIsImFsZyI6IlJTMjU2In0.eyJlbnRpdGxlbWVudHMiOltdLCJhdF9oYXNoIjoiZmZfMmxraXVBdDNONVhFaHE4dm0xUSIsInN1YiI6IjY2NjBjNzkxLTkwZWItNTlkMC1iNjJlLTcyYTg4ZThiNWY4MSIsImlzcyI6Imh0dHBzOlwvXC9lbnRpdGxlbWVudHMuYXV0aC5yaW90Z2FtZXMuY29tIiwiaWF0IjoxNjM5NDMxNzM3LCJqdGkiOiJBR1pJNEJlT0MyRSJ9.h8mvwsMrXBlwti9p2rPuB0_D3RQEI6gBz2olCzFMx8CUMxurqFWXzLWKNOCXAWQvAEnzpEULMePnc4NxW68cnfgTwap8rNLB6fsQSWQZ_CHqarO7R_v0cHcQ9-WUBT3BjA-CfwN6TmAqxKL1RkEHaaSU1LUjFrdo3Ji0i5PemFe3nEIVpHIDvXV1J-CxRrk7OM9MdmMoqBB1yglIIAKu--7XufkfaqeuLr3zR2CjOnoTAFTZuSMh1eccmZy6z1lBczbofimL0nn0QYL8Op0L2XdB5kZhZ9-INkbdsKHeU9f2z1WVL5gt2wRO1fqFmaC1Uiwmyl54HVluFZGJzydkWA',
                  '6660c791-90eb-59d0-b62e-72a88e8b5f81'],
         'test': ['eyJraWQiOiJzMSIsInR5cCI6ImF0K2p3dCIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiJmMTY1NWIzZS00NTY0LTViZWItYjU5OC0wZTg2ZDZmODZlZDgiLCJzY3AiOlsib3BlbmlkIl0sImNsbSI6WyJvcGVuaWQiXSwiZGF0Ijp7ImxpZCI6Il9Lc2RuVTdCeU4wRVNFVE1pYUU0Z2ciLCJjIjoiZWMxIn0sImlzcyI6Imh0dHBzOlwvXC9hdXRoLnJpb3RnYW1lcy5jb20iLCJleHAiOjE2Mzk0MzY1NjMsImlhdCI6MTYzOTQzMjk2MywianRpIjoiODZRNnV1VHZiUzAiLCJjaWQiOiJwbGF5LXZhbG9yYW50LXdlYi1wcm9kIn0.V41gDW0aNCRKjkFixiSTBeQf5MTmBziDusRGBBtEmW93MWhMU_ks44WCeaQxIoqZe2kIfXZCr9IbmH6NoOTUdY0ZwL3Pwcn6VsoNX_6nWqV62VNOvKkzXWTDBgJZkfRcgMjyBPpXLEHrU36eWX68sgULqMrfxjIusd0_4DjFO7c',
                  'eyJraWQiOiJrMSIsImFsZyI6IlJTMjU2In0.eyJlbnRpdGxlbWVudHMiOltdLCJhdF9oYXNoIjoib1dJSmIzcTM1VEpncjJvOW50d241USIsInN1YiI6ImYxNjU1YjNlLTQ1NjQtNWJlYi1iNTk4LTBlODZkNmY4NmVkOCIsImlzcyI6Imh0dHBzOlwvXC9lbnRpdGxlbWVudHMuYXV0aC5yaW90Z2FtZXMuY29tIiwiaWF0IjoxNjM5NDMyOTYzLCJqdGkiOiI4NlE2dXVUdmJTMCJ9.GM5GiLn7s3CYICDyGkKbnirxKYfiJ3b5T0_L2s20yO1HyCPVpQB8Ffo7lj3DDHaFO1VepB7K3pLstkgbKBL6qabK2dIHHg8wHs9rVFyGm-mdDZXgWyofHgG6Yvkf973XlJ3UHZxBVMmO2BZ5uvo5rVpRh0NZ3sbgtZYi-kcJZ76y4lriHYL430u-uR9w0S3Bx4TSva--jN6dltuC5-jawz3D7mPqE6fsT_sfYYUtzaK-rMeAnilBYRhoMLuc_M5pJlKFa1MM5hzu1_Sv--iO2hayR4RSymUsMufL2eH-Ca4dMGlHfkiA2kOeZOoPah0gpF6Nx2gJvgxNkvMVD1clRA',
                  'f1655b3e-4564-5beb-b598-0e86d6f86ed8'],
         'nat': ['eyJraWQiOiJzMSIsInR5cCI6ImF0K2p3dCIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiIzMjMwZWE0YS1hMGE2LTU3OWItODgzYS05N2UxNTFhZGNkMGIiLCJzY3AiOlsib3BlbmlkIl0sImNsbSI6WyJvcGVuaWQiXSwiZGF0Ijp7ImxpZCI6IjlHNk1jT2VPVDhTS2diX0ltSE5RSEEiLCJjIjoiZWMxIn0sImlzcyI6Imh0dHBzOlwvXC9hdXRoLnJpb3RnYW1lcy5jb20iLCJleHAiOjE2Mzk0MzgwNjksImlhdCI6MTYzOTQzNDQ2OSwianRpIjoiMWVXY3g5cXgwMDgiLCJjaWQiOiJwbGF5LXZhbG9yYW50LXdlYi1wcm9kIn0.g4cjf4hyn_Ukzb7OEhTY1BbvyM6iSCzUMCywFxmS1wVqFrEslBtHlKlQGBEwPlEvKyNWsVAkDZle4DBRYmVs_JQAhbTuw3v_69gXcZlTHP69cGo-sqlWLA7zCVXoAyaQCsbvDAAuVi8lNOU1ZYTK9e1W_C4DJ6Gj6kWMdYC8UGI',
                 'eyJraWQiOiJrMSIsImFsZyI6IlJTMjU2In0.eyJlbnRpdGxlbWVudHMiOltdLCJhdF9oYXNoIjoiaF9IZk5pbDNCTS1RTUZlSXhUNnVEQSIsInN1YiI6IjMyMzBlYTRhLWEwYTYtNTc5Yi04ODNhLTk3ZTE1MWFkY2QwYiIsImlzcyI6Imh0dHBzOlwvXC9lbnRpdGxlbWVudHMuYXV0aC5yaW90Z2FtZXMuY29tIiwiaWF0IjoxNjM5NDM0NDcwLCJqdGkiOiIxZVdjeDlxeDAwOCJ9.AFBIKAcrlZHkeTJCIme43N1bQ86ke_jrJfOocXm0QMKcq3rl5dFT6HCOOAnkxuFLBYvRyUEmzQeCaN6nWgeCdqE7psK_wkBd7ZqTdEzbuGwR5mbjzKUWvHyOk_UO0VI6PrQKZRBFtNia6nIjpnKA2aEzImmA0Ryzd1Bs8JYQWiNm6U4o4x1y7vmjGZpjtwQspMpZYAOIR21WYgo138aJ1KT7LWKTVkojk3OhiZhD0_nZY1n13xdHi45jGc0hN0rYP1qiFA_5lkUcVlIR28WXVP1xqZpj3zVDLlKOSie-gcfuiWpSi5jL_jO9vWmVZ61tGPbHoJEizc5KQZzAyk7Ghw',
                 '3230ea4a-a0a6-579b-883a-97e151adcd0b'],
         'kitty': ['eyJraWQiOiJzMSIsInR5cCI6ImF0K2p3dCIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiJiN2UyZjRhZS00MjdhLTUyMzAtYmY4My0zMGY3OGQyZDVlMTciLCJzY3AiOlsib3BlbmlkIl0sImNsbSI6WyJvcGVuaWQiXSwiZGF0Ijp7ImxpZCI6Ik5TeHVwYkZBbnRub0Q4N09Cc1ZVUlEiLCJjIjoiZWMxIn0sImlzcyI6Imh0dHBzOlwvXC9hdXRoLnJpb3RnYW1lcy5jb20iLCJleHAiOjE2Mzk0MzkyMzYsImlhdCI6MTYzOTQzNTYzNiwianRpIjoiUVotV2ZvdVBHLXMiLCJjaWQiOiJwbGF5LXZhbG9yYW50LXdlYi1wcm9kIn0.ea1qsPQFOadBGRM1_dhL1NQNDi56DH4otjPKdfaqftp-pUqQn0DawD83vz5xjt3kk9lBnsy-DdZSKEbYzapVMG5QcF3iDuAxL6pCfQtWhBn0rDn3FpsknaWrZ0HLlZnxMn3Y_cKsthh9Tl8ZYU8R-QrGKSP2CHtozfe5_KLlbbM',
                   'eyJraWQiOiJrMSIsImFsZyI6IlJTMjU2In0.eyJlbnRpdGxlbWVudHMiOltdLCJhdF9oYXNoIjoiTEktOHU2VnZqWkhDZUlwX1NocGM3dyIsInN1YiI6ImI3ZTJmNGFlLTQyN2EtNTIzMC1iZjgzLTMwZjc4ZDJkNWUxNyIsImlzcyI6Imh0dHBzOlwvXC9lbnRpdGxlbWVudHMuYXV0aC5yaW90Z2FtZXMuY29tIiwiaWF0IjoxNjM5NDM1NjM3LCJqdGkiOiJRWi1XZm91UEctcyJ9.YTqMu0sp9wh1MHzS51o_j9YxUwiNp7IK53NiJYLvnB3LCb-qrqO7of9XFEpG8-ML69s2ZuurmB1fKNR_7IvvnJPTTXbx4ytcNanqkcoO_Ukmr8lBAcXRF90Pyrp9fqD3O_oeGJy9pg2Y7A4MKFvsfwq50hSU6jC3I_0Hi8YmtsONaEp5uHm_gLte8tPRSnFmCOkLRDji8yUNqlQytnEEE3LiXBo9gztkRCiHk1Nez1btb5DtMA-Dsq03Dr6eecv-OHGzwfJwWlcsppy6wGamKA8QP0tcTQxg6gWPpmbtvSRm1aatZoaYU8cowaOZvALt-IYvHe64faY4mE3dlM5gQQ',
                   'b7e2f4ae-427a-5230-bf83-30f78d2d5e17']}

async def run(username, password, person):
    session = aiohttp.ClientSession()
    # data = {
    #     'client_id': 'play-valorant-web-prod',
    #     'nonce': '1',
    #     'redirect_uri': 'https://playvalorant.com/opt_in',
    #     'response_type': 'token id_token',
    # }
    # await session.post('https://auth.riotgames.com/api/v1/authorization', json=data)

    # data = {
    #     'type': 'auth',
    #     'username': input('please enter your username: '),
    #     'password': input('please enter your password: ')
    # }
    
    # async with session.put('https://auth.riotgames.com/api/v1/authorization', json=data) as r:
    #     data = await r.json()
    # pattern = re.compile('access_token=((?:[a-zA-Z]|\d|\.|-|_)*).*id_token=((?:[a-zA-Z]|\d|\.|-|_)*).*expires_in=(\d*)')
    # data = pattern.findall(data['response']['parameters']['uri'])[0]
    # access_token = data[0]
    
    userdata = users[person]
    access_token = userdata[0]
    entitlements_token = userdata[1]
    user_id = userdata[2]
    api_key = 'RGAPI-f3cd0ae7-b5e2-4e1d-ad20-9587c6165644'

    # headers = {
    #     'Authorization': f'Bearer {access_token}',
    # }
    # async with session.post('https://entitlements.auth.riotgames.com/api/token/v1', headers=headers, json={}) as r:
    #     data = await r.json()
    # entitlements_token = data['entitlements_token']

    # async with session.post('https://auth.riotgames.com/userinfo', headers=headers, json={}) as r:
    #     data = await r.json()
    # user_id = data['sub']
    # headers['X-Riot-Entitlements-JWT'] = entitlements_token
    
    headers3 = {"X-Riot-Token": api_key}
    async with session.get('https://eu.api.riotgames.com/val/content/v1/contents?locale=en-US', headers = headers3, json = {}) as r:
        data = await r.json()
    skins = data['skinLevels']
    ids = {}
    for skin in skins:
        ids[skin['id']] = skin['name']


    headers2 = {'Authorization': f'Bearer {access_token}', 'X-Riot-Entitlements-JWT': entitlements_token}
    async with session.get(f'https://pd.eu.a.pvp.net/store/v2/storefront/{user_id}', headers=headers2, json={}) as r:
        data = await r.json()
    shop = data['SkinsPanelLayout']
    items = shop['SingleItemOffers']
    store = []
    for item in items:
        store.append(ids[item.upper()])
        
    # print(access_token)
    # print('\n')
    # print(entitlements_token)
    # print('\n')
    # print(user_id)
    
    await session.close()
    return store

    

client = discord.Client()

@client.event
async def on_ready():
    print("online")
    
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    elif message.content.startswith('-store'):
        msg = message.content
        person = ''
        if msg.split('-store',1)[1] == ' will':
            person = 'will'
        elif msg.split('-store',1)[1] == ' nat':
            person = 'nat'
        elif msg.split('-store',1)[1] == ' kitty':
            person = 'kitty'
        elif msg.split('-store',1)[1] == ' new':
            pass
        elif msg.split('-store',1)[1] == ' test':
            person = 'test'
        else:
            await message.channel.send('Invalid Command Ending')
            return
        store = await run('exmaple user name', 'my_secret_password', person)
        storemessage = "Current Item Rotation:\n"
        for item in store:
            storemessage += item
            storemessage += '\n'
        await message.channel.send(storemessage)
        
client.run('OTIwMDUwNzc0MDk5MjMwNzUw.YbeuDg.zql4xg4XbSlFS6d_aY5wDe2gnqI')