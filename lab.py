"""
Lab — things built with AI, rather than designed for a client.

To add an entry, copy a block and drop a screenshot into
assets/lab/<slug>.jpg (1200px wide is plenty). Nothing else to touch:
build.py renders whatever is in this list, newest first.

Fields
    slug      used for the image filename
    added     YYYY-MM-DD it went on the site — the list sorts on this,
              newest first, so entries can be written in any order
    pin       "bottom" to hold an entry below the rest regardless of date
    status    "in-progress" puts an In progress label on the card
    business  True for a build that runs as a live business (real domain,
              real users or revenue): Live business label + filter
    title     what it is called
    kind      one-word category shown as a chip
    cats      filter groups on /lab/, any of: Landing, Website, Game, SaaS,
              Dashboard, E-commerce, Tools (the bar only shows groups in use)
    year      shown right-aligned
    blurb     one or two sentences — what it is and why it exists
    live      public URL, or None
    repo      source URL, or None
    stack     what it is actually built with
    ai        which models/tools did the heavy lifting
    notes     2-4 honest observations: what worked, what did not
"""

LAB = [

  dict(
    slug="postcraft-ai",
    added="2026-10-05",
    status="in-progress",
    business=True,
    title="PostCraft AI",
    kind="AI SaaS",
    cats=["SaaS"],
    year="2026",
    blurb="A social-post generator: type one topic, pick the platform, and get "
          "four image variants, a caption and a hashtag set sized for "
          "Instagram, TikTok, YouTube Shorts, X, Facebook or LinkedIn — with "
          "the image turned into a short loop for Reels in one click.",
    live="https://postcraft-ai-alpha.vercel.app/",
    repo=None,
    stack=["Next.js", "Gemini API", "Image to video"],
    ai=["Claude", "Gemini"],
    notes=[
      "The platform is chosen first, and everything downstream follows it: "
      "image ratio, caption length and the number of hashtags. The user "
      "never has to know that a story is 9:16 or that X cuts captions short.",
      "Four images instead of one. Picking from a grid is faster than "
      "rewriting a prompt, and it turns generation into a choice the user "
      "makes rather than a result they have to accept.",
      "Six languages including Georgian, written natively rather than "
      "translated after the fact — the same post in two languages should "
      "not read like a template.",
    ],
  ),

  dict(
    slug="space-odyssey",
    added="2026-10-01",
    title="Space Odyssey",
    kind="3D game",
    cats=["Game"],
    year="2026",
    blurb="A space shooter in the browser. Fly a fighter against enemy fleets "
          "that come for your homeworld in waves, then land, walk your base on "
          "foot and spend what you earned on turrets before the next wave.",
    live="https://easyvibesuxui-sketch.github.io/Space-odyssey/",
    repo=None,
    stack=["Three.js", "WebGL", "Web Audio"],
    ai=["Claude", "Kling"],
    notes=[
      "Two games in one loop: a cockpit for the fight and a walk around "
      "the home base on foot between waves. The quiet half is what "
      "makes the loud half feel earned — rewards are unloaded by hand, "
      "turrets are placed by hand.",
      "Every boss is a puzzle with one sentence of instruction: drones "
      "first, hangars first, shoot the glowing core, watch for the EMP. "
      "The HUD says what to do the moment it matters instead of in a "
      "manual nobody opens.",
      "The images, the coin, the icons and the preloader video were "
      "generated with Kling, and the credits screen says so.",
    ],
  ),

  dict(
    slug="waves-of-hell",
    added="2026-10-01",
    title="Waves of Hell",
    kind="Horror shooter",
    cats=["Game"],
    year="2026",
    blurb="A first-person wave shooter set in a dark station. Demons come in "
          "waves that never stop; between them you buy weapons and ammo at "
          "the armory, and a black dog fights beside you — if she goes down, "
          "you hold E to bring her back.",
    live="https://easyvibesuxui-sketch.github.io/Horror-game/",
    repo=None,
    stack=["Three.js", "Physics", "Web Audio"],
    ai=["Claude"],
    notes=[
      "The dog is the design decision. A companion you have to revive turns "
      "‘survive the wave’ into ‘protect someone’, and that changes how a "
      "player moves through the same corridors.",
      "Three slots — a pistol and two primaries — so a new weapon always "
      "costs you one you have. A limit is what makes a shop a choice.",
      "Enemies are sorted into three readable classes, easy, fast and "
      "brute, and the start screen names them. You know what is coming "
      "before you are scared of it.",
    ],
  ),

  dict(
    slug="sovereign",
    added="2026-10-01",
    title="Sovereign",
    kind="Strategy game",
    cats=["Game"],
    year="2026",
    blurb="A campaign of conquest on an old-atlas map — five realms, forty-two "
          "lands, one crown. Pick a people, place armies, attack, trade cards "
          "for reinforcements, and play against rivals at three temperaments.",
    live="https://easyvibesuxui-sketch.github.io/Game-Risk/",
    repo=None,
    stack=["React", "Turn-based engine", "Local saves"],
    ai=["Claude"],
    notes=[
      "A board game is mostly rules, so the interface is mostly sentences. "
      "Every illegal move answers in plain words — ‘a land needs at least "
      "two armies to attack’ — rather than a disabled button that leaves "
      "you guessing.",
      "The rivals are described by how they behave, not by a difficulty "
      "number: timid ones that strike rarely, ones that build continents, "
      "ruthless ones that hunt the leader.",
      "The look is an old atlas — cream paper, engraved portraits, Latin "
      "sea names. It makes a forty-two-territory screen calm to read.",
      "The campaign saves itself in the browser, so a long war can be "
      "left and picked up later.",
    ],
  ),

  dict(
    slug="boutique-raider",
    added="2026-10-01",
    title="Boutique Raider",
    kind="Arcade game",
    cats=["Game"],
    year="2026",
    blurb="A 3D runner through a luxury mall. Grab every shopping bag on the "
          "floor, dash past the Karens who want your manager, and make it to "
          "checkout — seven levels, each one adding a piece to the outfit.",
    live="https://easyvibesuxui-sketch.github.io/Shoprider/",
    repo=None,
    stack=["Three.js", "WebGL", "Keyboard controls"],
    ai=["Claude"],
    notes=[
      "The whole tutorial is one card: four keys and four rules. If it does "
      "not fit on that card, it is not in the game.",
      "Progress is something you can see on the character, not a number "
      "in the corner — each cleared level adds one piece to the outfit, "
      "and the HUD lists what is still to come.",
      "Three hearts and a dash that slips past an obstacle: one escape "
      "move, used well, is more fun than several half-used ones.",
    ],
  ),

  dict(
    slug="seu-development",
    added="2026-10-05",
    title="SEU Development",
    kind="Concept redesign",
    cats=["Website"],
    year="2026",
    blurb="A concept redesign for a Tbilisi residential developer — five projects "
          "from finished homes in Saburtalo to the new district in Varketili, an "
          "apartment search that starts from the view out of the window, and a "
          "360° look inside before anyone books a visit.",
    live="https://easyvibesuxui-sketch.github.io/Seu-development-refresh/",
    repo=None,
    stack=["Next.js", "Static export", "360° interior viewer"],
    ai=["Claude"],
    notes=[
      "The search opens on the view, not the floor plan: park, city, the "
      "Tbilisi Sea, mountains — then the number of bedrooms. People know what "
      "they want to see in the morning long before they know how many square "
      "metres they need.",
      "Every project card carries the same four facts — status with its date, "
      "district, apartment range, floors — so five buildings at five different "
      "stages compare at a glance.",
      "With off-plan sales the developer is the product. The about section "
      "leads with the one claim a buyer is weighing — every project funded "
      "from day one and delivered on time — and puts the finished university "
      "buildings right behind it as proof.",
    ],
  ),

  dict(
    slug="ibsu-applicants-animated",
    added="2026-10-05",
    title="IBSU — Applicants, animated cut",
    kind="Landing page",
    cats=["Landing"],
    year="2026",
    blurb="The same IBSU admissions landing page re-shot as an animated film: it "
          "opens on two children reading in a library of glowing marbles, the "
          "scroll plays the story forward age by age, and the page arrives at "
          "programmes, admission steps and the grant calculator.",
    live="https://easyvibesuxui-sketch.github.io/IBSU-Landing/c/",
    repo=None,
    stack=["GSAP + Lenis", "Scroll-scrubbed video", "Georgian / English"],
    ai=["Claude", "AI video"],
    notes=[
      "Variant C of one brief. The copy, the structure and the grant rules are "
      "identical to the holographic version — only the visual register "
      "changes, from cool hologram to warm animated characters. Two cuts of "
      "the same page let the school choose a tone without rewriting a word.",
      "Animated characters speak to the actual reader — a school-leaver and "
      "the parent sitting next to them — rather than to the institution’s "
      "picture of itself.",
      "‘Skip the story’ stays in the top bar from the first frame. The film "
      "is an invitation, never a gate in front of the fees.",
    ],
  ),

  dict(
    slug="ibsu-applicants",
    added="2026-10-01",
    title="IBSU — Applicants",
    kind="Landing page",
    cats=["Landing"],
    year="2026",
    blurb="An admissions landing page for International Black Sea University "
          "that opens as a story: a child grows up through the scroll, age by "
          "age, until the page arrives at the first day at university — then "
          "turns into programmes, admission steps and a grant calculator.",
    live="https://easyvibesuxui-sketch.github.io/IBSU-Landing/b/",
    repo=None,
    stack=["GSAP + Lenis", "Scroll-driven frames", "Georgian / English"],
    ai=["Claude", "Generative imagery"],
    notes=[
      "Another answer to the IBSU brief. The story is optional — ‘Skip the "
      "story’ sits in the top bar from the first frame, because the parent "
      "checking fees should not have to sit through a film made for their "
      "child.",
      "Admission is four steps, and the step that matters most says so: "
      "put IBSU, code 064, first at exam registration — it is what earns "
      "the 20% priority grant.",
      "The grant calculator applies only the highest single grant, the "
      "rule the university\u2019s own fee page states, so the figure on "
      "screen is not a best case nobody qualifies for.",
    ],
  ),

  dict(
    slug="lust-photography",
    added="2026-09-26",
    status="in-progress",
    title="Lust Photography",
    kind="AI studio",
    cats=["Landing"],
    year="2026",
    blurb="An AI photography studio with a Tuscan film look \u2014 sensual reels "
          "and stills of fictional muses, AI photoshoots for brands, and a "
          "web studio that builds creators their own platforms. Three "
          "businesses, one aesthetic, one page.",
    live="https://lustyphotography.com/",
    repo=None,
    stack=["Cloudflare Workers", "Blur-to-reveal gallery", "Lead forms"],
    ai=["Claude", "AI image + video"],
    notes=[
      "In progress \u2014 the gallery, the muses, the brand and creator offers "
      "and all three forms are standing; the content library is still "
      "being filled.",
      "Every tile loads blurred and opens on a click. That one decision "
      "makes the site safe to open anywhere and turns consent into a "
      "gesture the viewer makes per image rather than a box ticked once "
      "on the way in \u2014 the same idea as the hold-to-reveal gate on "
      "Maison Ondine, applied to a whole catalogue.",
      "The safeguards sit where the question arises, not in the terms. "
      "Each muse is labelled as an AI character and the cast section says "
      "every one is a fictional adult; the fantasy form asks for 18+, "
      "consenting adults and fictional characters right above the send "
      "button. A rule no one reads protects no one.",
      "Three audiences on one page is the real design problem. A brand "
      "buying a swimwear shoot is looking for a reason to leave, so that "
      "section says in one line that brand work is always fully clothed "
      "and safe for every platform \u2014 it answers the first objection "
      "before it is asked.",
      "Both offers carry real prices \u2014 \u20ac450, \u20ac950, \u20ac1,600 a month for "
      "brands, from \u20ac1,200 for creator sites. A named number lets the "
      "right client qualify themselves; \u2018get in touch\u2019 makes everyone "
      "do a call first.",
    ],
  ),


  dict(
    slug="uxaudit-ai",
    added="2026-09-24",
    status="in-progress",
    title="UXAudit AI",
    kind="SaaS",
    cats=["SaaS"],
    year="2026",
    blurb="Paste a URL and get a senior-level UX and CRO audit in about "
          "thirty seconds \u2014 graded against WCAG 2.1 and Nielsen\u2019s ten "
          "heuristics, with every finding ranked by impact divided by "
          "effort so you know what to do first.",
    live="https://uxaudit-ai.easyvibesuxui.workers.dev/",
    repo=None,
    stack=["Cloudflare Workers", "Vision + LLM passes", "PDF export"],
    ai=["Claude", "Vision"],
    notes=[
      "In progress \u2014 URL and screenshot audits run, Flow Mode and the "
      "paid tiers are still being finished.",
      "AI design feedback is usually adjectives: \u2018the hierarchy could be "
      "clearer\u2019. Useless. Every finding here has to carry a number \u2014 "
      "2.1:1, 913px, 69px past the fold, the exact success criterion "
      "violated. A measurement can be argued with and acted on; an "
      "adjective can only be nodded at.",
      "Ranking by impact \u00f7 effort is what makes it a tool rather than a "
      "report. Twenty findings paralyse; three that are high-impact and "
      "ten minutes of CSS get done this afternoon, which is the only "
      "version of an audit that changes anything.",
      "The section I am most pleased with is the one where the site audits "
      "itself. The buttons are light blue with dark text because white on "
      "mid-blue tops out at 5.2:1 \u2014 AA, not AAA. The conventional choice "
      "would have failed the product\u2019s own test, and saying so out loud "
      "is worth more than any trust badge.",
      "Pricing is framed against the thing it replaces: an agency audit is "
      "$2,000 and two weeks. Naming the alternative does the persuading, "
      "so the plans themselves can just list what you get.",
      "Failed audits are never charged and the copy says so. The failure "
      "case is where a tool like this earns or loses trust \u2014 a credit "
      "burned on a page we could not even reach is exactly the moment "
      "someone cancels.",
    ],
  ),


  dict(
    slug="giftly",
    added="2026-09-24",
    status="in-progress",
    business=True,
    title="Gifty",
    kind="AI search",
    cats=["Tools"],
    year="2026",
    blurb="A gift finder you describe a person to, not a product. You write "
          "\u201cmy dad who won\u2019t stop talking about coffee\u201d the way you\u2019d text "
          "a friend, and it reads the sentence for meaning rather than "
          "matching keywords.",
    live="https://askgifty.com/gifts/",
    repo=None,
    stack=["Vector search", "Gemini embeddings", "Cloudflare Pages"],
    ai=["Claude", "Gemini"],
    notes=[
      "In progress \u2014 the search, the curated shelf and the affiliate model "
      "are standing; the counters on the landing page still read zero "
      "because they are wired to real numbers that have not arrived yet, "
      "rather than being filled with flattering placeholders.",
      "Every gift site asks what you want to buy. Nobody knows what they "
      "want to buy \u2014 that is the entire problem. Asking who the person is "
      "instead is the whole product, and it only works because embeddings "
      "can match on meaning where a keyword index cannot.",
      "The prompt examples do the teaching: \u2018Mom who gardens\u2019, \u2018Techie "
      "boyfriend, under $50\u2019. An empty box with an AI behind it is "
      "intimidating; four sample sentences show the register to write in "
      "faster than any instruction would.",
      "No account, nothing stored, free. A gift search is a once-a-year "
      "panic, and a signup wall in front of a panic loses the user. The "
      "affiliate cut pays for it, and the footer says so plainly instead "
      "of burying it in the terms.",
      "One testimonial, not a wall of them. \u2018He actually cried\u2019 is the "
      "outcome the product sells; adding nine more would have made all ten "
      "read as invented.",
    ],
  ),


  dict(
    slug="inverse",
    added="2026-09-11",
    title="Inverse",
    kind="B2B services + platform",
    cats=["Landing"],
    year="2026",
    blurb="A Tbilisi stocktaking firm, and the tool its own counters use. A "
          "worker photographs a shelf, the system reads the still, counts what "
          "it can see per SKU and says how sure it is \u2014 then a person decides.",
    live="https://inverse-xi.vercel.app/ka",
    repo=None,
    stack=["Next.js", "Multi-tenant DB", "Vision on stills"],
    ai=["Claude", "Vision"],
    notes=[
      "The platform pricing is shown as awaiting commercial sign-off rather "
      "than quietly presented as final \u2014 a number a client might plan "
      "around should say when it is not settled yet.",
      "The verification runs on a still frame, not a live stream. A frame is "
      "the thing that gets stored, re-checked and shown to an auditor months "
      "later; a stream is gone the moment it plays. For a count that has to "
      "be defensible, evidence beats immediacy.",
      "Every SKU gets a verdict rather than a guess: green matches, yellow "
      "needs a human, red means the record is wrong. Nothing reaches the "
      "ledger without a person confirming it \u2014 an inventory system that "
      "silently writes its own numbers is a liability, not a feature.",
      "The interesting part is where the camera is admitted to be useless. "
      "Two products from one line are identical at a metre and differ only "
      "in size, so those get flagged for a barcode check with the likely "
      "candidates named. Saying \u2018I cannot tell these apart\u2019 is worth more "
      "than a confident wrong count.",
      "Tenants are isolated at the database level rather than by code that "
      "might forget a filter. With client stock figures, that is the "
      "difference between an architecture and a hope.",
      "Written in Georgian first, with English and Russian alongside \u2014 the "
      "buyers are warehouse and retail managers in Tbilisi.",
    ],
  ),

  dict(
    slug="wedding-platform",
    added="2026-09-23",
    status="in-progress",
    business=True,
    title="\u10dd\u10e0\u10d8 \u10d2\u10e3\u10da\u10d8 \u2014 Two Hearts",
    kind="Product",
    cats=["SaaS"],
    year="2026",
    blurb="A Georgian platform for digital wedding invitations. Pick a "
          "template, write your own words, send one link \u2014 and the replies "
          "come back as a list instead of ninety separate text messages.",
    live="https://www.brideinvitation.com/",
    repo=None,
    stack=["Next.js", "Multi-tenant publishing", "i18n \u00d7 3"],
    ai=["Claude"],
    notes=[
      "This started as one invitation for one couple. Building it made the "
      "product obvious: everything except the names, the date and the "
      "photographs was the same work every time. The single site became the "
      "template engine.",
      "The line that sells it is the one about paper: a paper invitation "
      "ends up under glass, a link stays in the pocket until the day. That "
      "is the whole argument for the category, and it fits in a sentence.",
      "RSVP is the feature people actually pay for, even though templates "
      "are what they browse. Counting guests from scattered replies is the "
      "worst week of planning a wedding \u2014 here the guest answers on the "
      "same page they were invited on, and the couple sees one list with "
      "headcount and dietary notes already in it.",
      "Language is detected from the guest\u2019s phone rather than asked. "
      "Georgian, English and Russian, with the switch still in the corner "
      "for anyone it guessed wrong about. A language picker as the first "
      "screen of an invitation is a toll gate on a gift.",
      "Templates are fully openable before you buy \u2014 you walk through one "
      "exactly as a guest would, envelope to last frame. Thumbnails would "
      "have been cheaper and would have sold nothing: the thing being sold "
      "is a sequence, so it has to be experienced as one.",
      "Custom design is priced at 50\u20be as a one-off: send three photographs "
      "and say what you want. Naming a number, rather than \u2018contact us\u2019, "
      "is what turns a portfolio piece into a business.",
    ],
  ),

  dict(
    slug="treasure-marathon",
    added="2026-09-03",
    title="\u10e1\u10d0\u10d2\u10d0\u10dc\u10eb\u10e3\u10e0\u10d8\u10e1 \u10db\u10d0\u10e0\u10d0\u10d7\u10dd\u10dc\u10d8 \u2014 Treasure Marathon",
    kind="Campaign concept",
    cats=["Landing"],
    year="2026",
    blurb="A campaign concept for TBC that turns four money habits into four "
          "noble houses. A treasure shatters into coins across the kingdom, "
          "the houses race to collect them, and a quiz tells you which one "
          "you have been all along.",
    live="https://easyvibesuxui-sketch.github.io/TBCLegend/",
    repo=None,
    stack=["Next.js", "Tailwind", "Scroll-driven sections"],
    ai=["Claude", "AI video"],
    notes=[
      "Banks talk about saving and spending in the language of product "
      "features, which nobody adopts as an identity. Houses people do "
      "adopt. Kharjiani spends because life happens once, Anabaridze "
      "insures the future, Dovlatia chases luck, Baratishvili keeps the "
      "old order \u2014 four financial behaviours, none of them written as the "
      "wrong answer.",
      "That last part is the constraint the whole thing is built on. The "
      "moment one house is the sensible one, the quiz becomes a scolding "
      "and the campaign becomes a lecture. Every motto had to be "
      "defensible from inside the house.",
      "The leaderboard is what turns a personality quiz into a season: "
      "your result stops being a private label and becomes a side you are "
      "adding a coin to. It is placeholder data here, but the mechanic is "
      "the point \u2014 a bank campaign that has standings has a reason to be "
      "checked twice.",
      "Written in Georgian first, with the English house names underneath "
      "rather than the other way round. A myth told in translation is "
      "somebody else\u2019s myth.",
      "The whole arc is three scroll acts \u2014 prologue, the night it "
      "shattered, the marathon \u2014 before a single house appears. Front-"
      "loading the story is what earns the quiz at the end; leading with "
      "\u2018take our quiz\u2019 would have got the usual answer.",
    ],
  ),


  dict(
    slug="maison-ondine",
    added="2026-09-03",
    title="Maison Ondine",
    kind="Lingerie e-commerce",
    cats=["E-commerce"],
    year="2026",
    blurb="A lingerie house where the shop mechanics are the product. "
          "Hold-to-reveal instead of an age-gate button, motion backgrounds "
          "behind the collection, and a score written for the site rather than "
          "licensed onto it \u2014 the video and the music are both mine, made with "
          "AI tools.",
    live="https://easyvibesuxui-sketch.github.io/EroticAD/",
    repo=None,
    stack=["HTML + CSS", "Vanilla JS", "Scroll-driven video", "Web Audio"],
    ai=["Claude", "AI video + music"],
    notes=[
      "Still in progress \u2014 the gate, the identity, the score and Collection "
      "Premi\u00e8re are standing; the rest of the shop is being built.",
      "Lingerie sells badly in a normal product grid: a flat thumbnail on white "
      "tells you nothing about how a piece moves or sits. So the browsing "
      "mechanic is built on motion \u2014 video behind the collection rather than "
      "stills in a matrix, which is the one thing a photograph cannot do.",
      "Compliance screens are usually designed by nobody. This one is the "
      "brief: hold to reveal, so entry is a deliberate physical action instead "
      "of a mis-tapped button, and the tone is set before a single product "
      "appears.",
      "I wrote the music with an AI tool rather than licensing a track. A "
      "stock loop makes any brand sound like every other brand \u2014 and for a "
      "house whose whole proposition is intimacy, borrowed atmosphere is "
      "exactly the wrong signal. Same reasoning for the video: generated to "
      "the brand, not bought off a shelf.",
      "Sound is offered, never autoplayed. On a site like this it is the one "
      "element that can genuinely embarrass someone, so it stays a choice \u2014 "
      "which also means the score has to earn the tap.",
    ],
  ),

  dict(
    slug="terramech",
    added="2026-08-30",
    title="TerraMech",
    kind="Brand site",
    cats=["Website", "Game"],
    year="2026",
    blurb="A site for a fictional heavy-plant maker whose company history is "
          "locked. You run an arcade shift on the yard \u2014 catch the loads, "
          "keep hazards out of the bucket \u2014 and your salvage total unseals "
          "the six pages of the record one at a time.",
    live="https://easyvibesuxui-sketch.github.io/minigame/",
    repo=None,
    stack=["HTML + CSS", "Vanilla JS", "Canvas game loop", "Web Audio"],
    ai=["Claude"],
    notes=[
      "The premise is one inversion of a normal About page: nobody reads a "
      "company timeline, so the timeline is earned. Six entries, most of them "
      "sealed, opening as the score rises \u2014 the copy even says it out loud: "
      "\u2018Nobody reads our history. They earn it.\u2019",
      "Because the history is the reward, the writing had to be worth "
      "unlocking. Each entry is a real turn in how a machine company would "
      "change \u2014 the first rebuilt dragline, the day everything got painted "
      "signal red because it was the only paint the yard held in quantity.",
      "The game is deliberately simple \u2014 one axis, mouse or arrows, three "
      "power-ups. Anything more and people would play instead of read, which "
      "would defeat the point of the mechanic.",
      "It is a fictional client, which is the freedom: no brand guidelines to "
      "satisfy, so every decision had to be justified by the idea alone.",
    ],
  ),

  dict(
    slug="nami",
    added="2026-08-30",
    title="NAMI",
    kind="Hospitality",
    cats=["Landing"],
    year="2026",
    blurb="A bathhouse and mountain garden at 2,025 m on the Goderdzi Pass \u2014 "
          "twelve saunas, four waters and a ritual timetable where something "
          "begins every half hour. Georgian-rooted, written to be read slowly.",
    live="https://easyvibesuxui-sketch.github.io/SPa/",
    repo=None,
    stack=["HTML + CSS", "Vanilla JS", "Scroll-driven animation"],
    ai=["Claude"],
    notes=[
      "\u10dc\u10d0\u10db\u10d8 means dew, and the whole identity comes from that one word: a "
      "serif set at whisper weight, brass on near-black, and a mark that is a "
      "single drop. Naming the brand in Georgian first made every other "
      "decision easier.",
      "The hard part of a spa site is that the product is an absence \u2014 no "
      "noise, no hurry, nothing to do. So the specifics carry it instead: "
      "eight degrees chest deep for thirty seconds, Black Sea salt carried up "
      "from Batumi, nine hundred candles lit at dusk.",
      "The ritual timetable is the structure rather than a feature list. "
      "\u2018Every half hour, something begins\u2019 turns a menu of services into a "
      "reason to stay, which is what the business actually sells.",
      "Pacing is done with scroll rather than motion. Long holds, wide "
      "measure, very little movement \u2014 a site about slowness that animates "
      "eagerly would be arguing with itself.",
    ],
  ),


  dict(
    slug="chalet",
    added="2026-08-25",
    title="Chalet",
    kind="Marketing site",
    cats=["Landing"],
    year="2026",
    blurb="A landing page for a fictional alpine villa atelier, built around one "
          "idea: the hero is an ink blueprint of a chalet that draws itself in as "
          "you scroll. Fourteen sections, a build sequence from survey to first "
          "fire, and a preloader that says \u2018drawing the blueprint\u2019.",
    live="https://easyvibesuxui-sketch.github.io/Chalet/",
    repo=None,
    stack=["HTML + CSS", "Vanilla JS", "Canvas", "Scroll-driven animation"],
    ai=["Claude"],
    notes=[
      "The whole site hangs off one metaphor. \u2018Scroll to build\u2019 in the hero and a "
      "BLUEPRINT progress rail along the bottom mean the scrollbar is reframed as "
      "construction \u2014 and the five process sections (survey, structure, stone, "
      "envelope, keys) inherit that reading without needing to explain it.",
      "Copy did more for the tone than any effect. \u2018We draw it in winter. You live "
      "in it by the next one\u2019 and \u2018cozy is an engineering decision\u2019 set a register "
      "that the visuals then only have to keep, which is much easier than "
      "generating atmosphere from motion alone.",
      "The hero is a canvas, not an image, so it scales without a 4MB render and "
      "the line work stays crisp at any width. That was the right call for a "
      "drawing and would have been the wrong one for a photograph.",
      "It is a fictional client, which is the point \u2014 no brand guidelines, no "
      "stakeholder, so every decision had to be justified by the idea alone.",
    ],
  ),


  dict(
    slug="khomeriki-design",
    added="2026-08-02",
    title="khomeriki.design",
    kind="Portfolio",
    cats=["Website"],
    year="2026",
    blurb="This site. A portfolio with no framework and no page builder — "
          "a Python script generates thirty static pages from one shell, and "
          "the motion runs on hand-written WebGL and GSAP.",
    live="https://khomeriki.design",
    repo=None,
    stack=["Python generator", "Vanilla JS", "WebGL", "GSAP + Lenis", "CSS"],
    ai=["Claude"],
    notes=[
      "The background is a GPU particle field. The reference implementation I "
      "started from advected 50,000 particles in a JavaScript loop; moving the "
      "whole simulation into a vertex shader dropped it to one draw call and "
      "12KB, instead of the 600KB three.js would have cost.",
      "Every page comes from one build script, so the nav, footer and meta can "
      "never drift apart. Editing content means editing a Python list.",
      "Vibe coding gets you to a running thing fast, then the real work starts: "
      "most of the time here went on contrast, layout drift and cache headers — "
      "the parts a demo never has to survive.",
    ],
  ),

  dict(
    slug="ga-logistics",
    added="2026-08-22",
    title="GA Logistics",
    kind="Redesign",
    cats=["Website"],
    year="2026",
    blurb="A redesign for a New Jersey trucking carrier — 200 power units, "
          "48 states, eight services and one dispatch desk. The brief was not "
          "to make a haulage company look like a tech startup, but to make ten "
          "years of real capacity legible to a broker deciding in thirty "
          "seconds.",
    live="https://easyvibesuxui-sketch.github.io/GALogisticsRedesign/",
    repo=None,
    stack=["Static site", "Video hero", "Horizontal scroll", "Multi-page"],
    ai=["Claude", "Code generation", "Copy"],
    notes=[
      "Freight buyers are checking one thing: can you actually move this. So "
      "the numbers lead — ten years, two hundred power units, forty-eight "
      "states, 24/7 dispatch — and the strongest line on the site is the "
      "one that says what those numbers mean: when we commit to a load, the "
      "truck exists.",
      "Eight services is too many for a menu and exactly right for a sideways "
      "scroll. Turning the range into something you move through rather than "
      "read down let each one keep a full card without the page becoming a "
      "list of eight identical blocks.",
      "The copy does the differentiating, not the layout. ‘Asset-based "
      "carrier’, ‘founded by drivers with 7 and 14 years on the "
      "road’, ‘the people answering the phone at 3am’ — "
      "in a market where every competitor claims reliability, the specific "
      "thing is the only convincing thing.",
      "Two yards and a dark, photographic treatment do the rest. Trucking "
      "sites default to blue gradients and stock highways; shooting the actual "
      "fleet against near-black is both more honest and, for once, cheaper.",
    ],
  ),

  dict(
    slug="ibsu-international",
    added="2026-08-22",
    title="IBSU — International Admission",
    kind="Concept",
    cats=["Landing"],
    year="2026",
    blurb="A fourth answer to the IBSU brief, this time for the students "
          "arriving from abroad: twenty-six English-taught degrees, the "
          "documents you have to notarise, and the five steps between an "
          "enquiry and a residence permit.",
    live="https://romanibsu.netlify.app/",
    repo=None,
    stack=["Scroll narrative", "Mosaic imagery", "Web"],
    ai=["Claude", "Generative imagery"],
    notes=[
      "International admission is an anxiety problem before it is a marketing "
      "one. Somebody deciding to move countries needs to know what to send, "
      "what it costs and what happens next — so the page is structured as "
      "requirements and steps rather than as reasons to come.",
      "The one detail that mattered most is repeated where it applies: every "
      "document must be notarised and translated into Georgian. That single "
      "sentence is the difference between an application that proceeds and one "
      "that comes back, and it is usually buried in a PDF.",
      "The classical staging — Roman numerals, a mosaic that shifts as you "
      "scroll, a golden road for the five steps — gives an ordinary "
      "admissions page the weight of an institution. It is the same argument "
      "as the marble concept, made for a different reader.",
      "It closes on the International Relations Office rather than on a form, "
      "with a footnote telling applicants to verify tuition and deadlines "
      "before submitting. A concept page about someone’s visa should not "
      "pretend to be authoritative about their visa.",
    ],
  ),

  dict(
    slug="syniotec-devices",
    added="2026-08-16",
    title="Syniotec — Devices",
    kind="Product site",
    cats=["Website"],
    year="2026",
    blurb="A showroom for seven telematics units that go on construction "
          "machinery — wired boxes reading the CAN bus, self-powered "
          "trackers, and passive tags with no battery at all. The hardware "
          "counterpart to the Syniotec platform I design, built as a scroll "
          "narrative where the exploded parts assemble as you read.",
    live="https://easyvibesuxui-sketch.github.io/Land-Game-IBSu-/",
    repo=None,
    stack=["Next.js", "Static export", "Scroll-driven render sequence",
           "GitHub Pages"],
    ai=["Claude", "Code generation", "Generative product imagery"],
    notes=[
      "Seven SKUs is past the number anybody can hold in their head, so the "
      "range is presented as three classes first — wired, powered, "
      "passive — and only then as seven units. The classification is the "
      "product decision; the grid underneath is just the consequence.",
      "The exploded board assembling on scroll is the argument, not the "
      "decoration. It says these are one range built from the same parts, "
      "which is the claim a hardware line has to make before any single spec "
      "matters.",
      "Every unit gets one sentence and then the numbers that back it. "
      "‘Reads the machine, not just the map.’ ‘Five years "
      "without a thought.’ ‘No battery. No radio. Still tracked.’ "
      "A spec sheet nobody reads becomes a spec sheet somebody remembers when "
      "each device is allowed a position rather than a paragraph.",
      "The footer states what the site refuses to be: hardware only, no "
      "pricing, no forms. A showroom that does not chase you is a stronger "
      "sales tool for equipment bought by engineers than one that does — "
      "and it is the reason the whole thing could stay this quiet.",
      "It pairs with the SAM and RAM platforms in my work section: these are "
      "the devices sending the data those interfaces spend their time making "
      "legible. Designing both ends of the same system is rarer than it "
      "should be, and it changes what you notice at each end.",
    ],
  ),

  dict(
    slug="my-toolkits",
    business=True,
    pin="bottom",
    added="2026-08-10",
    title="My ToolKit",
    kind="AI-built · Ad-funded",
    cats=["Tools"],
    year="2026",
    blurb="Thirty-four browser utilities — JSON formatter, HEIC converter, PDF "
          "merge, hash generator, colour and contrast checker — every one of "
          "them running on the user's own device. Front end, tooling logic, "
          "copy, translations into nine languages and the SEO were all "
          "produced with AI; my job was deciding what to build and what "
          "the rules were.",
    live="https://my-toolkits.com/",
    repo=None,
    stack=["Client-side JS", "Canvas &amp; Web Crypto", "Nine languages",
           "Schema.org", "AdSense"],
    ai=["Claude", "Code generation", "Copy &amp; SEO", "Translation"],
    notes=[
      "The whole product is one promise: nothing is uploaded. HEIC decoding "
      "runs on the device's own graphics stack, hashes come from Web Crypto, "
      "PDFs are assembled in memory. That is not a privacy policy, it is an "
      "architecture — there is no upload endpoint to trust, because none was "
      "ever written.",
      "Thirty-four tools is only viable because they share one shell: the same "
      "input panel, the same result block, the same copy and download actions. "
      "Generating the thirty-fifth is cheap; deciding it belongs is the part "
      "that still takes judgement.",
      "Every tool ships with its own long-form explainer and FAQ, and the "
      "structured data is written so that search engines and assistants can "
      "quote the answer directly. When a chatbot is the front page, being "
      "quotable matters more than ranking.",
      "The honest constraint: this is ad-funded, so the incentive is traffic "
      "rather than depth, and free runs are rate-limited to keep costs sane. "
      "Naming that in the interface — three runs, share to skip — beats "
      "letting someone discover the limit mid-task.",
    ],
  ),

  dict(
    slug="myclacks",
    business=True,
    pin="bottom",
    added="2026-08-10",
    title="myclacks",
    kind="AI-built · Ad-funded",
    cats=["Tools"],
    year="2026",
    blurb="Financial calculators — mortgage, loan, compound interest, "
          "retirement, tax, salary, debt-to-income — in fourteen languages "
          "across the US, Canada, UK and EU, wrapped in three dozen guides "
          "that do the actual ranking. Built, written, localised and "
          "optimised with AI.",
    live="https://myclacks.com/",
    repo=None,
    stack=["Static site", "Client-side maths", "Fourteen locales",
           "Programmatic SEO", "AdSense"],
    ai=["Claude", "Code generation", "Copy &amp; SEO", "Translation"],
    notes=[
      "The calculators are the product; the guides are the distribution. "
      "Nobody searches for 'mortgage calculator' and reads — they search "
      "'how much house can I afford on 100k' and want an answer. So each "
      "guide answers the question in prose and hands the reader the tool that "
      "does their own numbers.",
      "Fourteen locales is not fourteen translations. Tax brackets, currency, "
      "date order and what counts as a normal mortgage term all differ, so "
      "the localisation had to reach the maths, not just the labels.",
      "Money tools are trust tools. Everything is calculated locally, no "
      "account exists, and the formulas are named in the copy — a user who "
      "can see it is amortisation rather than a black box is a user who "
      "comes back.",
      "What I would change: the tool list grew faster than the navigation "
      "did. Generation makes adding easy and pruning invisible, and a "
      "duplicated percentage calculator sitting in two sections is exactly "
      "the kind of drift that follows.",
    ],
  ),

  dict(
    slug="belly-bell",
    business=True,
    pin="bottom",
    added="2026-08-10",
    title="Belly Bell",
    kind="AI-built · Ad-funded",
    cats=["Tools"],
    year="2026",
    blurb="Pregnancy and fertility calculators — due date, ovulation, fertile "
          "window, contraction timer, week-by-week tracking — in six "
          "languages, with an editorial layer around them. The narrowest of "
          "the three, and the one where the writing had to be handled most "
          "carefully.",
    live="https://belly-bell.com/en/",
    repo=None,
    stack=["Static site", "Client-side maths", "Six locales",
           "Editorial content", "AdSense"],
    ai=["Claude", "Code generation", "Copy &amp; SEO", "Translation"],
    notes=[
      "A niche audience with high intent beats a broad one. Someone working "
      "out a due date is at the start of a nine-month stretch of searches — "
      "which is why the tools sit next to a blog rather than alone.",
      "This is health-adjacent content, so the tone had to be governed rather "
      "than generated freely. Naegele's rule is named, the estimate is framed "
      "as a window rather than a date, the Chinese gender predictor is "
      "labelled as entertainment with no scientific basis, and every page "
      "defers to a midwife or obstetrician. AI will happily write in a more "
      "confident voice than the subject deserves; the editorial rules exist "
      "to stop it.",
      "Nothing is stored and no account exists — for cycle and pregnancy "
      "dates that is not a feature, it is the minimum. The calculations never "
      "leave the browser.",
      "The three sites share one recipe: pick a question people already "
      "search, answer it with a tool that runs locally, write the "
      "surrounding page properly, translate it, and let it earn while you "
      "sleep. Belly Bell is the version where I had to argue with the "
      "generated draft the most.",
    ],
  ),

  dict(
    slug="classygreens",
    added="2026-08-09",
    title="ClassyGreens",
    kind="AI-operated",
    cats=["Website"],
    year="2026",
    blurb="A visual atelier that runs itself. Every image, every film, every "
          "line of copy and the site around them are generated — and the "
          "publishing keeps going week after week without a photographer, a "
          "studio or a shoot day. The closest thing I have to a proof that an "
          "entire brand can be operated by one person and a set of models.",
    live="https://www.classygreens.com/",
    repo=None,
    stack=["Sanity CMS", "Structured content", "Trilingual DE / EN / RU",
           "Programmatic SEO", "Web"],
    ai=["Image generation", "Video generation", "Claude", "Copy &amp; SEO"],
    notes=[
      "This is the part that interests me: it is not a one-off generated site, "
      "it is a production line. A new series is generated, written, "
      "translated, tagged and published on a weekly rhythm — so the question "
      "stopped being 'can AI make an image' and became 'can AI hold a "
      "publishing schedule'. It can, but only because the content is modelled "
      "properly first.",
      "Nothing is a page. Projects, models and journal entries are structured "
      "records in a CMS, which is why one generated series can fan out into a "
      "project page, a model's history, a listing card, an Instagram crop and "
      "its own metadata without anyone assembling those by hand.",
      "Models are treated as recurring characters rather than one-time "
      "outputs. Each has a profile and a project history, so the work "
      "accumulates into a body of work instead of a feed — that continuity is "
      "the hardest thing to get out of generative tooling and the thing that "
      "makes the brand feel like a studio.",
      "SEO is generated with the work, not bolted on after: titles, "
      "descriptions and canonicals per record, in three languages, so every "
      "new series arrives already indexable. Volume is only an advantage if "
      "each item can be found on its own.",
      "The interface earns its keep too. Premium frames are revealed by "
      "dragging across them like a scratch card, rationed to three a day — a "
      "deliberate friction that makes an infinite supply of images feel "
      "finite, which is the whole economic problem with generated work.",
      "The disclosure is the position, not the small print. An 'AI' mark sits "
      "in the header, the footer says it plainly, and the front door is an "
      "18+ advisory. Naming the tool is more interesting than hiding it — and "
      "the site is only as credible as the thing it admits to being.",
    ],
  ),

  dict(
    slug="ibsu-ink-gallery",
    added="2026-08-08",
    title="IBSU — The Ink Gallery",
    kind="Playable",
    cats=["Game"],
    year="2026",
    blurb="A university prospectus you walk through. An ink stickman crosses a "
          "hand-drawn hall lined with six doors — Programs, Fees, Admission, "
          "Tuition, Relocation, International — and pushing one open takes you "
          "to that part of IBSU admissions.",
    live="https://ibsu-ink-gallery.netlify.app/",
    repo=None,
    stack=["Canvas", "Vanilla JS", "Hand-drawn assets", "Web"],
    ai=["Claude", "Generative imagery"],
    notes=[
      "The third answer to the same IBSU brief, and the one that stops "
      "pretending to be a website. Navigation is a room: six doors instead of "
      "six nav links, and a counter that tells you how many you have opened.",
      "Everything is ink on paper — the pen strokes carry the whole art "
      "direction, so there is no photography to source and nothing to look "
      "dated in two years.",
      "Games have onboarding costs a website does not, so the controls are "
      "taught three ways at once: keyboard, an on-screen joystick, and simply "
      "clicking the floor. Clicking is the one nobody has to be told about.",
      "Honest limitation: it takes about fifteen seconds to load and it asks "
      "for effort before it gives anything back. That is the right trade for a "
      "school-leaver browsing at midnight and the wrong one for a parent "
      "checking tuition — which is exactly why it sits beside two "
      "conventional proposals rather than replacing them.",
    ],
  ),

  dict(
    slug="ibsu-entrant",
    added="2026-08-02",
    title="IBSU — Entrant",
    kind="Concept",
    cats=["Landing"],
    year="2026",
    blurb="An admissions site aimed squarely at school-leavers rather than at "
          "the university. Five scroll chapters — Vision, Programs, Admission, "
          "Funding, Apply — that end on the Georgian national-exam steps, "
          "because that is the actual decision an applicant has to make.",
    live="https://ibsu-entrant-cd-b8aa2ec2e0.netlify.app/",
    repo=None,
    stack=["Scroll narrative", "Composite imagery", "Web"],
    ai=["Claude", "Generative imagery"],
    notes=[
      "Universities usually sell themselves to parents. This one addresses the "
      "seventeen-year-old: one question in the hero, then the enrolment path in "
      "three concrete steps instead of a prospectus.",
      "Classical sculpture composited into a dark, gilded field — an attempt at "
      "an academic institution that does not look like every other one.",
      "The chapter rail doubles as a progress indicator, so the page tells you "
      "how much decision is left before you commit to reading it.",
    ],
  ),

  dict(
    slug="ibsu-wisdom",
    added="2026-08-02",
    title="IBSU — Wisdom, carved in stone",
    kind="Concept",
    cats=["Landing"],
    year="2026",
    blurb="The same brief taken the opposite way: marble instead of night, a "
          "serif voice, and the institution's numbers doing the talking. Built "
          "as a counter-proposal so the choice between the two was a decision "
          "rather than the first idea.",
    live="https://merry-blini-9467f3.netlify.app/",
    repo=None,
    stack=["Editorial layout", "Serif type system", "Web"],
    ai=["Claude", "Generative imagery"],
    notes=[
      "Two directions for one brief is the cheapest thing a designer can do and "
      "the one clients value most — it turns 'do you like it' into 'which one'.",
      "Stone, owl and quiet gold do the institutional work that a stock photo of "
      "smiling students usually fails at.",
      "Known issue: at some widths the hero headline breaks mid-word — 'carved "
      "in ston / e.' A word-break rule set too aggressively on the display type.",
    ],
  ),

]
