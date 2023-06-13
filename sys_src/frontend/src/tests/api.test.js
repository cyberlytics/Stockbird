import React from 'react';
import { callAPITweets } from '../pages/api';

describe('Testing the Tweet API call', () => {
    jest.setTimeout(60000);
    test('Tweets should be defined after calling the API', async () => {
        const control = '_query_tweets_by_substring';
        //Here you can give some substrings like 'Tesla' or 'Bitcoin' to check if the substring occurs in the data from the backend
        const substring = 'Dogecoin';

        const result = await callAPITweets(control, substring);
        const parsedResult = JSON.parse(result);

        // With this line, you can see the 'data' column in the console. Be aware that there could be many tweets.
        console.log('API Result:', parsedResult.data);

        expect(parsedResult.data).toBeDefined();
    });
});