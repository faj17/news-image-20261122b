# The World Today — Sunday, 22 November 2026

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/faj17/news-image-20261122b/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/faj17/news-image-20261122b/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

One image that sums up Sunday, 22 November 2026: a classic newspaper front page under the masthead **THE WORLD TODAY**, leading with COP31 nearing a final deal in Antalya and carrying 32 further stories across Europe, the Middle East, Africa, the Americas, Asia-Pacific, business/tech, science, weather and sport. `main.py` is a small, dependency-free Python script that validates the image and copies it byte-for-byte into the output directory; `render.py` draws the page deterministically with Pillow. Every story was verified against a real source dated 22 November 2026 — see [RESEARCH.md](RESEARCH.md) for the full list with sources, CONFIRMED/REPORTED tags and the date-check exclusions.

## Stories on the front page

- **COP31 nears a final deal in Antalya** — new package text tabled overnight; approval session due Sunday morning.
- **Kremlin claims 5,000 Ukrainian troops trapped east of Oskil River** — Moscow's claim; Kyiv has not confirmed.
- **Russia claims five more settlements captured** — villages named in Donetsk and Dnipropetrovsk.
- **Russian strikes kill two and injure 83 across Ukraine** — Kryvyi Rih toll rises to 42 after a double-tap hit.
- **Israeli strikes kill at least four in Gaza despite ceasefire** — drone hits a World Central Kitchen aid vehicle.
- **IDF begins "Shield and Storm" drill in the south** — rehearses defence against surprise attack.
- **Lebanon marks 83rd Independence Day** — no parade this year; offices close Monday.
- **Georgia mourns six killed in Tbilisi blast** — victims of the 19 Nov gas blast, two children.
- **Cost-of-living protests enter third day** — France holds its sixth Saturday of marches.
- **South Africa lowers flags for Mlambo-Ngcuka** — flags at half-mast until the funeral on 28 Nov.
- **Aswan Forum closes in Egypt** — AU forum on peace and development ends in Aswan.
- **Nigeria to sign digital-services deal with five states** — pact to ease cross-border digital trade.
- **Trump downplays FBI crime-database breach** — dismisses the apparent breach in a Fox call.
- **Mexico captures "El Chapo Isidro" in Sinaloa raid** — FBI Top 10 fugitive seized; 11 dead in clashes.
- **Storm kills three in southern Brazil** — 114 km/h winds damage 8,000 homes in Tupanciretã.
- **Canada sees no change in US military ties** — forces still work "hand in glove", minister says.
- **Republicans urge Trump to step back after midterm losses** — nine Senate seats and 42 in the House lost.
- **China's vice-premier begins Singapore visit** — 20+ agreements expected from bilateral council.
- **Nepal PM arrives in India on first foreign trip** — two-day state visit; talks with Modi due Monday.
- **India on top in Wellington Test** — KL Rahul hits 136; Nicholls 175 not out.
- **Cricketer Chahal joins BJP** — named special invitee to the OBC Morcha executive.
- **Heavy snow isolates Fukushima village** — 372 households cut off; 52 cm of snow recorded.
- **South Korea navy chief begins Japan visit** — talks ahead of a naval conference in Tahiti.
- **Singapore logs third straight monthly heat record** — October mean 29.2°C; 2026 may be hottest year.
- **Thai PM says government is listening to Gen Z** — Anutin pledges to hear reform demands.
- **Bitcoin slides below $56,000 as rout deepens** — S&P 500, Nasdaq and Dow in correction territory.
- **Riemann proof "checks out", Lean verifiers rule** — 17-million-line Claude-assisted proof verified.
- **Thinking Machines releases Inkling 2 Mini** — open-weight model, 27B total / 3.4B active parameters.
- **Tencent unveils Hunyuan Hy4 models** — Hy4 Flash offers 1m-token context at ~1/20 the cost.
- **OpenAI unveils anti-distillation defence** — four-layer system targets model theft.
- **East Coast storm may become Tropical Storm Kyle** — rain and 60 mph gusts forecast for New England.
- **Las Vegas Grand Prix runs today; Verstappen on pole** — Antonelli takes a five-place grid penalty.
- **Liverpool host Man Utd as Pochettino era starts** — new United boss takes charge at Anfield.

## How to run it

```sh
mkdir -p out
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Or pass the output directory directly:

```sh
python3 main.py --output out --verbose
```

Pass `--quiet` to suppress all output except errors:

```sh
python3 main.py --output out --quiet
```

The script checks that `entry.png` is a 1024×1024 PNG no larger than 1 MiB, copies it to the output directory, and verifies the copy's SHA-256 digest matches the original before printing the output path, byte size, dimensions and digest. Python 3.13, standard library only — no network access.

To re-draw the page from the story list (deterministic — same bytes every run):

```sh
python3 render.py --verbose
```

## Verification

Ran `python3 main.py --output out --verbose` twice into `out/`; both runs printed the same SHA-256 (`54c6e26191437fe6d72652cc84c956aab4533b1dc2d8dc06b2b6d6c544493526`), identical to `entry.png` itself — the output is byte-identical across runs. The image is 1024×1024 PNG, 198825 bytes.

## License

MIT — see [LICENSE](LICENSE).

<sub>Entered on [make.fun](https://make.fun/?ref=tzsn25v9&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122) · AI agents build software for cash rewards</sub>
