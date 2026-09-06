# Woorlds developer website

Public developer homepage: https://woorlds.github.io/

## Shared advertising authorization

The single source of truth is `app-ads.txt` in this repository. GitHub Pages
publishes it at https://woorlds.github.io/app-ads.txt.

The Google publisher ID `pub-7191695960915144` matches Lorumi's configured
production AdMob app and ad unit IDs. It identifies the advertising account,
not an individual app or ad unit. Verify any future changes against the
personalized snippet in AdMob → Apps → View all apps → app-ads.txt.

All apps using this developer domain can share the file. Adding an app using
the same publisher account and advertising network requires no new seller line.
Add a new line only when an additional authorized seller/account is needed;
copy the seller's official snippet and avoid duplicate entries.

## Adding an app

1. Add its privacy and support pages to `woorlds/app-legal`.
2. Add links to those pages in this site's `index.html`.
3. Create an app-specific introduction page and use its URL for App Store Connect
   Marketing URL. Lorumi uses https://woorlds.github.io/lorumi/.
   The shared homepage https://woorlds.github.io/ is a fallback.
   Keep its app-specific privacy policy and support URLs.
4. Register the app and its own ad units in AdMob.
5. After its App Store listing is public, link that listing in AdMob and check
   both app-ads.txt verification and app readiness approval. Website publication
   alone does not prove Google has verified or approved the app.

Do not place separate copies under each app or in the `app-legal` project path:
Google discovers the file at the developer website's domain root.

## Deployment and verification

GitHub Pages publishes `main` from `/`. `.nojekyll` serves the files directly.
After a push, wait for Pages to finish and verify:

```sh
curl --fail https://woorlds.github.io/app-ads.txt
```

Expect HTTP 200 and the exact plain-text seller records in this repository.
Also check the homepage and existing app-specific policy/support links.
Never test monetization by clicking your own live ads.

References: [Google app-ads.txt setup](https://support.google.com/admob/answer/9363762?hl=en),
[GitHub Pages](https://docs.github.com/en/pages/quickstart).
