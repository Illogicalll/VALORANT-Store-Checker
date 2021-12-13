import re
import aiohttp
import asyncio
import json


async def run(username, password):
    session = aiohttp.ClientSession()
    data = {
        'client_id': 'play-valorant-web-prod',
        'nonce': '1',
        'redirect_uri': 'https://playvalorant.com/opt_in',
        'response_type': 'token id_token',
    }
    await session.post('https://auth.riotgames.com/api/v1/authorization', json=data)

    data = {
        'type': 'auth',
        'username': input('please enter your username: '),
        'password': input('please enter your password: ')
    }
    
    async with session.put('https://auth.riotgames.com/api/v1/authorization', json=data) as r:
        data = await r.json()
    pattern = re.compile('access_token=((?:[a-zA-Z]|\d|\.|-|_)*).*id_token=((?:[a-zA-Z]|\d|\.|-|_)*).*expires_in=(\d*)')
    data = pattern.findall(data['response']['parameters']['uri'])[0]
    access_token = data[0]
    print('\n')
    print('Access Token: \n' + access_token)
    print('\n')
    id_token = data[1]
    expires_in = data[2]

    headers = {
        'Authorization': f'Bearer {access_token}',
    }
    async with session.post('https://entitlements.auth.riotgames.com/api/token/v1', headers=headers, json={}) as r:
        data = await r.json()
    entitlements_token = data['entitlements_token']
    print('Entitlements Token: \n' + entitlements_token)
    print('\n')

    async with session.post('https://auth.riotgames.com/userinfo', headers=headers, json={}) as r:
        data = await r.json()
    user_id = data['sub']
    print('User ID: \n' + user_id)
    print('\n')
    headers['X-Riot-Entitlements-JWT'] = entitlements_token
    
    headers3 = {"X-Riot-Token": "RGAPI-f3cd0ae7-b5e2-4e1d-ad20-9587c6165644"}
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
    print("Current Item Roatation:")
    for item in items:
        print(ids[item.upper()])
    print('\n')
    
    await session.close()

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(run('exmaple user name', 'my_secret_password'))