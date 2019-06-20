# AmmonomiconBot

AmmonomiconBot is a Reddit bot (found at [u/AmmonomiconBot](https://www.reddit.com/user/AmmonomiconBot)) which provides useful information about Enter The Gungeon content (pulled from [the official wiki)](https://enterthegungeon.gamepedia.com/Enter_the_Gungeon_Wiki) when requested.

## Using the bot

The bot will look for wiki entries in all comments posted in [r/EnterTheGungeon](https://www.reddit.com/r/EnterTheGungeon/). In order to send a request to the bot, the entry has to be put inside braces. One comment can contain multiple requests.

E.g:

![A simple request](https://i.imgur.com/5eOqrfC.png)

![Multiple requests in a single comment](https://i.imgur.com/PK8bdiI.png)

## Info Provided

The bot will provide different info depending on the entry category. The bot will only provide info for enemies *(bosses excluded)*, guns and items.

**Enemies**: Art, Description, Base Health, Link to Wiki

**Guns**: Art, Quote, Description, Quality, Type, Magazine Size, Damage, Fire Rate, Reload Time, Shot Speed, Range, Force, Spread, Link to Wiki

**Items**: Art, Quote, Description, Quality, Type, Link to Wiki

## How it works

When the bot finds one or more requests, it looks in the database for the likeliest entry using fuzzy search. If there's more than one request in a comment, all search results will be displayed in a single reply. The bot will also provide helpful links at the end of the comment (FAQs, bug report, etc.).
