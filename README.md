![Test](https://github.com/yohanesgultom/notify-slack-action/workflows/Test/badge.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# Notify Slack Action

Send Github Actions workflow status notifications to Slack.

### Example workflow

Put this step at the end of your workflow:

```yaml
steps:

  # your other steps
  # your other steps
  # your other steps

  - uses: yohanesgultom/notify-slack-action@master
    if: always()
    with:
      status: ${{ job.status }}
      notify_when: 'failure' # default: 'success,failure,warnings'
    env:
      SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }} # required
      COMMIT_MESSAGE: ${{ github.event.head_commit.message }} # get head commit message
      GITHUB_TOKEN: ${{ secrets.PERSONAL_TOKEN }} # override authentication
```



<sub>Originally Made in Python &bull; By [Ravgeet Dhillon](https://github.com/ravgeetdhillon) @ [RavSam Web Solutions](https://www.ravsam.in).</sub>
<sub>Message customization By &bull; By [Yohanes](https://github.com/yohanesgultom).</sub>
