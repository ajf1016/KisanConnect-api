const { BotFrameworkAdapter } = require('botbuilder');
const restify = require('restify');

// Create adapter to connect bot to Microsoft Bot Framework
const adapter = new BotFrameworkAdapter({
    appId: process.env.MicrosoftAppId || '',
    appPassword: process.env.MicrosoftAppPassword || ''
});

// Create a Restify server
let server = restify.createServer();
server.listen(3978, function () {
    console.log(`\nBot is listening on http://localhost:3978`);
});

// Create a bot that will respond to messages
server.post('/api/messages', async (req, res) => {
    await adapter.processActivity(req, res, async (context) => {
        // Process incoming messages
        if (context.activity.type === 'message') {
            const message = context.activity.text.toLowerCase();

            if (message.includes('hello')) {
                await context.sendActivity('Hi! Are you a farmer or a corporation?');
            } else if (message.includes('farmer')) {
                await context.sendActivity('How can I assist you today? (Product info, Troubleshooting, Crop advice, etc.)');
            } else if (message.includes('corporation')) {
                await context.sendActivity('What can I help you with? (Order status, Partnership inquiries, Technical support, etc.)');
            } else {
                await context.sendActivity('I didn’t understand that. Can you please clarify?');
            }
        }
    });
});
