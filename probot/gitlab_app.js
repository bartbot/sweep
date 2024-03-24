import { GitLabClient } from 'gitlab';
import OAuth2Strategy from 'passport-oauth2';

const gitLabClient = new GitLabClient({
    oauth2: {
        clientId: process.env.GITLAB_CLIENT_ID,
        clientSecret: process.env.GITLAB_CLIENT_SECRET,
        callbackURL: process.env.GITLAB_CALLBACK_URL,
    },
});

function initializeGitLabApp() {
    gitLabClient.use(new OAuth2Strategy({
        authorizationURL: 'https://gitlab.com/oauth/authorize',
        tokenURL: 'https://gitlab.com/oauth/token',
        clientID: gitLabClient.oauth2.clientId,
        clientSecret: gitLabClient.oauth2.clientSecret,
        callbackURL: gitLabClient.oauth2.callbackURL,
    }, (accessToken, refreshToken, profile, cb) => {
        gitLabClient.accessToken = accessToken;
        return cb(null, profile);
    }));

    gitLabClient.on('issue', async (data) => {
        const projectID = data.project.id;
        const issueIID = data.object_attributes.iid;
        await gitLabClient.Issues.createNote(projectID, issueIID, {
            body: 'Thanks for opening this issue!',
        });
    });
}

initializeGitLabApp();
