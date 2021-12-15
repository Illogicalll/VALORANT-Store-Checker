import re
import aiohttp
import asyncio


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
    
    print("available regions: eu (europe), na (north america), ap (asia pacific), ko (korea)")
    region = input('please enter your region: ')
    options = ['eu', 'na', 'ap', 'ko']
    valid = False
    while valid == False:
        if region.lower() not in options:
            region = input('invalid choice please pick from either eu, na, ap, ko: ')
        else:
            region = region.lower()
            valid = True
    
    async with session.put('https://auth.riotgames.com/api/v1/authorization', json=data) as r:
        data = await r.json()
    pattern = re.compile('access_token=((?:[a-zA-Z]|\d|\.|-|_)*).*id_token=((?:[a-zA-Z]|\d|\.|-|_)*).*expires_in=(\d*)')
    data = pattern.findall(data['response']['parameters']['uri'])[0]
    access_token = data[0]

    headers = {
        'Authorization': f'Bearer {access_token}',
    }
    async with session.post('https://entitlements.auth.riotgames.com/api/token/v1', headers=headers, json={}) as r:
        data = await r.json()
    entitlements_token = data['entitlements_token']
    async with session.post('https://auth.riotgames.com/userinfo', headers=headers, json={}) as r:
        data = await r.json()
    user_id = data['sub']
    headers['X-Riot-Entitlements-JWT'] = entitlements_token
    
    async with session.get('https://api.henrikdev.xyz/valorant/v1/content?locale=en-US', headers=None, json={}) as r:
        data = await r.json()
        skins = data['skinLevels']
    ids = {}
    for skin in skins:
        ids[skin['id']] = skin['name']


    headers2 = {'Authorization': f'Bearer {access_token}', 'X-Riot-Entitlements-JWT': entitlements_token}
    async with session.get(f'https://pd.{region}.a.pvp.net/store/v2/storefront/{user_id}', headers=headers2, json={}) as r:
        data = await r.json()
    shop = data['SkinsPanelLayout']
    items = shop['SingleItemOffers']
    print('\n')
    print("Current Item Roatation:\n")
    for item in items:
        print(ids[item.upper()])
    print('\n')
    
    await session.close()

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(run('exmaple user name', 'my_secret_password'))