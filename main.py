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
    headers = {
        "Accept": "*/*",
        "User-Agent": username
    }
    try:
        await session.post('https://auth.riotgames.com/api/v1/authorization', json=data, headers=headers)
    except Exception as e:
        print(e)

    data = {
        'type': 'auth',
        'username': username,
        'password': password
    }
    
    try:
        async with session.put('https://auth.riotgames.com/api/v1/authorization', json=data, headers=headers) as r:
            data = await r.json()
    except Exception as e:
        print(e)
    try:
        if "type" in data:
            if (data["type"] == 'multifactor'):
                return 405, 405
        if "error" in data:
            if (data["error"] == 'auth_failure'):
                return 403, 403
            elif(data["error"] == 'rate_limited'):
                return 429, 429
        pattern = re.compile(
            'access_token=((?:[a-zA-Z]|\d|\.|-|_)*).*id_token=((?:[a-zA-Z]|\d|\.|-|_)*).*expires_in=(\d*)')
        data = pattern.findall(data['response']['parameters']['uri'])[0]
        access_token = data[0]

        headers = {
            'Authorization': f'Bearer {access_token}',
            "User-Agent": username
        }

        try:
            async with session.post('https://entitlements.auth.riotgames.com/api/token/v1', headers=headers, json={}) as r:
                data = await r.json()
        except Exception as e:
            print(e)
        entitlements_token = data['entitlements_token']
        try:
            async with session.post('https://auth.riotgames.com/userinfo', headers=headers, json={}) as r:
                data = await r.json()
        except Exception as e:
            print(e)

        user_id = data['sub']
        headers['X-Riot-Entitlements-JWT'] = entitlements_token
        headers['X-Riot-ClientPlatform'] = "ew0KCSJwbGF0Zm9ybVR5cGUiOiAiUEMiLA0KCSJwbGF0Zm9ybU9TIjogIldpbmRvd3MiLA0KCSJwbGF0Zm9ybU9TVmVyc2lvbiI6ICIxMC4wLjE5MDQyLjEuMjU2LjY0Yml0IiwNCgkicGxhdGZvcm1DaGlwc2V0IjogIlVua25vd24iDQp9"
        headers['X-Riot-ClientVersion'] = "pbe-shipping-55-604424"
    except Exception as e:
        print(e)

    headers2 = {'Authorization': f'Bearer {access_token}', 'X-Riot-Entitlements-JWT': entitlements_token, 'Content-Type': 'text/plain'}
        
    json2 = [user_id]
    async with session.get(f'https://pd.eu.a.pvp.net/store/v2/storefront/{user_id}', headers=headers2, json=json2) as r:
        data = await r.json()
    shop = data['SkinsPanelLayout']
    items = shop['SingleItemOffers']

    rotation = []
    for item in items:
        async with session.get(f'https://valorant-api.com/v1/weapons/skinlevels/{item}', headers=headers) as r:
            data = await r.json()
        rotation.append(data['data']['displayName'])
    
    print('\nCurrent Item Rotation:')
    for skin in rotation:
        print(skin)
        
    await session.close()

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(run(input('Riot ID: '), input('Password: ')))

input('Press Enter to Exit...')