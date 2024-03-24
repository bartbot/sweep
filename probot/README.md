# sweep-self-deploy

> This is a fork of Probot adapted for GitLab to easily set up a GitLab App with the right permissions for self-hosting Sweep.

## Setup

Follow these GitLab-specific steps to get started:
1. Register your application in GitLab to obtain your Application ID and Secret.
2. Configure your application's callback URL in GitLab.
3. Install the GitLab App dependencies:

```sh
npm install && npm start
```

## Contributing

If you have suggestions for how self-deploying could be improved, or want to report a bug, open an issue! We'd love all and any contributions.

## Transition from GitHub to GitLab

The transition from GitHub to GitLab was made to leverage GitLab's integrated CI/CD and issue tracking features, providing a more seamless experience for managing and deploying applications. Notable differences include the setup process and the way permissions are handled in GitLab compared to GitHub.

## License

[ISC](LICENSE) © 2023 Kevin Lu
