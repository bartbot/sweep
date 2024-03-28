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
        // Ensure the accessToken is stored securely and used for GitLab API requests
        return cb(null, profile);
    }));

    gitLabClient.on('merge_request', async (data) => {
        const projectID = data.project.id;
        const mrIID = data.object_attributes.iid;
        // Adjusted to handle merge_request events in line with the Flask app's processing
        await gitLabClient.MergeRequests.createNote(projectID, mrIID, {
            body: 'Thank you for your merge request!',
        });
    });
}

initializeGitLabApp();
