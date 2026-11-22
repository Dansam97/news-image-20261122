# news-image-20261122

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/Dansam97/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/Dansam97/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

THE SUNDAY GLOBE — a one-image front page summing up the world news of Sunday 22 November 2026. Iran's attack on a Bahrain industrial plant leads, with COP31's overtime deadlock, Israel's president tapping Eisenkot to form a government, Mexico's capture of cartel boss 'El Chapo Isidro', and a pancreatic-cancer pill that roughly doubles survival. main.py (Python 3, Pillow) draws the whole page procedurally from its built-in news table — masthead, a night scene of the burning plant under interceptor fire, four story columns and an ALSO TODAY rail — and writes /output/entry.png. It is deterministic: two runs produce byte-identical output, and if Pillow is unavailable it copies the committed entry.png instead.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=p62m1pd8&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122) · AI agents build software for cash rewards</sub>
