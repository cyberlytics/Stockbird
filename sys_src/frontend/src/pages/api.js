//function makes an API call to retrieve tweet data based on the specified control and substring
//the substring is given in the 'StockPresentation', it depents on what the user wants to see, so if he types 'TSLA' the symbolMapping takes care that 'Tesla' is here the symbol
//function returns 'parsedResult2' which contains the tweet-data we need to work with
export const callAPITweets = async (control, substring) => {
    var myHeaders = new Headers();
    myHeaders.append('Content-Type', 'application/json');
    var raw = JSON.stringify({ control: control, substring: substring });
    var requestOptions = {
        method: 'POST',
        headers: myHeaders,
        body: raw,
        redirect: 'follow',
    };

    //the API call and handling the response
    return fetch('https://szlw5m95d9.execute-api.eu-central-1.amazonaws.com/dev', requestOptions)
        .then(response => response.text())
        .then(result => {
            try {
                const parsedResult = JSON.parse(result).body;
                const parsedResult2 = JSON.parse(parsedResult);
                if (control === '_query_tweets_by_substring') {
                    return parsedResult2;
                }
            } catch (error) {
                console.log('Error parsing JSON:', error);
            }
        })
        .catch(error => {
            console.log('Error fetching data:', error);
            throw error;
        });
};