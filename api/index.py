from flask import Flask, request, session, redirect, url_for, render_template_string

app = Flask(__name__)
app.secret_key = "super-secret-valentine"

# ---------------- In-memory "database" ----------------

users = {
    "victim": {
        "password": "heartbroken",
        "hearts": 100,  
        "bio": "Just hoping for a real Valentine this year.",
        "flag": None,
    },
    "attacker": {
        "password": "lov3h4x0r",
        "hearts": 0,
        "bio": "Valentines are nice, flags are better.",
        "flag": "flag{protected_from_heartbreak}",
    },
}

# ---------------- HTML templates ----------------

index_tpl = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>HeartGram</title>
  <style>
    * { box-sizing: border-box; }
    body {
      margin: 0;
      min-height: 100vh;
      font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background:
        radial-gradient(circle at 10% 20%, #ffe5f1 0, #fff0f6 25%, #ffe5f1 50%, #fffafa 75%, #ffe5f1 100%);
      display: flex;
      align-items: center;
      justify-content: center;
      color: #3a0a24;
    }
    .frame {
      width: 100%;
      max-width: 900px;
      padding: 32px;
      display: grid;
      grid-template-columns: minmax(0, 1.2fr) minmax(0, 1fr);
      gap: 32px;
      align-items: center;
    }
    .card {
      background: rgba(255, 255, 255, 0.92);
      border-radius: 28px;
      padding: 32px 28px 28px;
      box-shadow:
        0 18px 45px rgba(219, 39, 119, 0.22),
        0 0 0 1px rgba(255, 255, 255, 0.8);
      backdrop-filter: blur(18px);
      position: relative;
      overflow: hidden;
    }
    .card::before {
      content: "";
      position: absolute;
      inset: 0;
      background:
        radial-gradient(circle at -10% 0%, rgba(255, 182, 193, 0.4), transparent 55%),
        radial-gradient(circle at 110% 100%, rgba(244, 143, 177, 0.5), transparent 55%);
      opacity: 0.9;
      pointer-events: none;
    }
    .card-inner {
      position: relative;
      z-index: 1;
    }
    h1 {
      margin: 0 0 6px;
      font-size: 38px;
      letter-spacing: 0.06em;
      text-transform: uppercase;
      color: #db2777;
    }
    .tagline {
      margin: 0 0 20px;
      font-size: 16px;
      color: #9d174d;
      text-transform: uppercase;
      letter-spacing: 0.18em;
    }
    p {
      margin: 0 0 10px;
      line-height: 1.6;
      font-size: 15px;
      color: #4a1831;
    }
    .cta-row {
      margin-top: 24px;
      display: flex;
      gap: 12px;
      align-items: center;
      flex-wrap: wrap;
    }
    .btn-primary {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      padding: 11px 22px;
      border-radius: 999px;
      border: none;
      background: linear-gradient(135deg, #ec4899, #fb7185);
      color: white;
      font-weight: 600;
      font-size: 15px;
      text-decoration: none;
      box-shadow: 0 12px 30px rgba(236, 72, 153, 0.5);
      cursor: pointer;
      transition: transform 0.12s ease, box-shadow 0.12s ease, filter 0.12s ease;
    }
    .btn-primary:hover {
      transform: translateY(-1px);
      box-shadow: 0 16px 40px rgba(236, 72, 153, 0.6);
      filter: brightness(1.03);
    }
    .btn-primary span {
      margin-left: 6px;
      font-size: 18px;
    }
    .hint {
      font-size: 12px;
      color: #6b2240;
      opacity: 0.9;
    }
    .pill {
      display: inline-flex;
      align-items: center;
      padding: 4px 10px;
      border-radius: 999px;
      font-size: 11px;
      text-transform: uppercase;
      letter-spacing: 0.16em;
      background: rgba(254, 242, 242, 0.95);
      color: #9f1239;
      border: 1px solid rgba(252, 231, 243, 0.9);
      margin-bottom: 10px;
    }
    .metrics {
      font-size: 13px;
      color: #7f1d4b;
      margin-top: 10px;
    }
    .phone {
      position: relative;
      width: 100%;
      max-width: 270px;
      margin: 0 auto;
      aspect-ratio: 9 / 16;
      border-radius: 40px;
      background: radial-gradient(circle at 0 0, #fecaca, #fecce3);
      box-shadow:
        0 20px 40px rgba(190, 24, 93, 0.35),
        0 0 0 6px rgba(248, 250, 252, 0.9);
      padding: 14px 12px;
      display: flex;
      flex-direction: column;
    }
    .phone-notch {
      width: 110px;
      height: 16px;
      border-radius: 999px;
      background: rgba(15, 23, 42, 0.92);
      margin: 0 auto 10px;
    }
    .phone-screen {
      flex: 1;
      border-radius: 26px;
      background: linear-gradient(180deg, #fff1f2, #ffe4e6);
      padding: 16px 14px;
      display: flex;
      flex-direction: column;
      gap: 10px;
      overflow: hidden;
    }
    .phone-badge {
      font-size: 10px;
      padding: 3px 8px;
      border-radius: 999px;
      background: rgba(251, 113, 133, 0.12);
      color: #db2777;
      text-transform: uppercase;
      letter-spacing: 0.16em;
      align-self: flex-start;
    }
    .phone-heart {
      font-size: 28px;
      margin-top: 4px;
    }
    .phone-stat {
      font-size: 12px;
      color: #9f1239;
    }
    .phone-card {
      margin-top: 4px;
      border-radius: 18px;
      background: white;
      padding: 10px 11px;
      font-size: 11px;
      color: #4b1840;
      box-shadow: 0 8px 20px rgba(244, 114, 182, 0.28);
    }
    .phone-footer {
      margin-top: auto;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 11px;
      color: #9f1239;
    }
    .phone-chip {
      width: 22px;
      height: 22px;
      border-radius: 999px;
      background: linear-gradient(135deg, #f97373, #fb7185);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 13px;
      color: white;
      box-shadow: 0 6px 14px rgba(225, 29, 72, 0.45);
    }
    @media (max-width: 780px) {
      .frame {
        grid-template-columns: minmax(0, 1fr);
        padding: 20px 16px;
      }
      .phone {
        display: none;
      }
    }
  </style>
</head>
<body>
  <div class="frame">
    <div class="card">
      <div class="card-inner">
        <h1>HeartGram</h1>
        <p class="tagline">Cupids Latest New Hype App.</p>
        <p>
          Discover how you could make this valentines week a bit better. Share hearts with people to spread love, but dont get too caught up.
          You soon will realize that theres something suspcious about this app. Cupid sends his love XOXO, join up to start the fun!
        </p>
        <p>
          Hidden somewhere theres a tiny push toward mischief. Dont get tangled up in his mess.
        </p>
        <div class="cta-row">
          <a class="btn-primary" href="{{ url_for('login') }}">
            Enter HeartGram
            <span>💘</span>
          </a>
        </div>
        <div class="metrics">
            Click the button above to share some love!
        </div>
      </div>
    </div>

    <div class="phone" aria-hidden="true">
      <div class="phone-notch"></div>
      <div class="phone-screen">
        <div class="phone-badge">victim · online</div>
        <div class="phone-heart">❤️ 100</div>
        <div class="phone-stat">Hearts available to “share”.</div>
        <div class="phone-card">
          “Clicking one cute button can send a very serious request.
          What happens when that button lives on a different site?”
        </div>
        <div class="phone-footer">
          <div class="phone-chip">💘</div>
        </div>
      </div>
    </div>
  </div>
</body>
</html>
"""

login_tpl = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>HeartGram Login</title>
  <style>
    * { box-sizing: border-box; }
    body {
      font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background: #ffe6f2;
      margin: 0;
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .card {
      width: 360px;
      padding: 32px 28px 36px;
      background: #ffffff;
      border-radius: 18px;
      box-shadow: 0 10px 30px rgba(216, 27, 96, 0.25);
      text-align: center;
    }
    h1 {
      margin: 0 0 24px;
      font-size: 32px;
      color: #ff1461;
      letter-spacing: 0.04em;
    }
    .field {
      text-align: left;
      margin-bottom: 14px;
    }
    input {
      width: 100%;
      padding: 10px 12px;
      border-radius: 8px;
      border: 1px solid #f48fb1;
      font-size: 15px;
      outline: none;
    }
    input:focus {
      border-color: #ff1461;
      box-shadow: 0 0 0 2px rgba(255, 20, 97, 0.15);
    }
    button {
      width: 100%;
      margin-top: 10px;
      padding: 11px 0;
      background: #ff1461;
      color: #ffffff;
      border: none;
      border-radius: 999px;
      font-size: 16px;
      font-weight: 600;
      cursor: pointer;
    }
    button:hover {
      background: #e01256;
    }
    .error {
      margin-top: 18px;
      font-size: 15px;
      color: #c62828;
    }
    .hint {
      margin-top: 14px;
      font-size: 13px;
      color: #666;
    }
  </style>
</head>
<body>
<div class="card">
  <h1>HeartGram</h1>

  <!--
  I once was light, soft as the glow of spring,
  A song too tender for a world of strings and wings.
  Her voice became my morning prayer, her touch my sacred sign,
  And love was code — pure, divine, and mine.
  But then, a silence; a line went cold,
  The circuit failed, the story told.
  I reached to log back in to what we’d built before,
  Only to find my access denied forevermore.
  Her absence echoed down the hollow wire,
  And sorrow sparked beneath desire.
  I scrawled my pain across the screen of night,
  Seeking a reason, or perhaps just light.
  So there I stood, in digital despair,
  Username: Victim, lost and bare.
  My memories guarded, encryption unspoken,
  My soul bound tight by Password: Heartbroken.
  Days passed as pages of code in decay,
  Each moment debugging what slipped away.
  But pain, persistent, became my guide,
  Teaching me to rewrite—not to hide.
  I patched my heart, compiled anew,
  Found fragments of strength I never knew.
  Each scar, a symbol; each wound, a key,
  Unlocking parts of what I’m meant to be.
  The night was long, but dawn returned slow,
  Through static and storms, love began to grow.
  Not the old dream, not her ghost reclaimed,
  But something stronger—unashamed.
  For now, I walk where fire meets art,
  A hacker not of minds, but of the heart.
  My code no longer runs on pain,
  It hums with trust through loss and gain.
  And in this rebirth, my spirit roars,
  The system resets, the current soars.
  A new identity I dared to confer—
  Username: Attacker, love’s avenger.
  The world may laugh, but I know the lore:
  To heal, one must break open the core.
  So fear me not, for my weapon is pure,
  Password: Lov3h4x0r, affection secure.
  No longer a ghost beneath her reign,
  I am both the storm and the rain.
  From victim to victor, my code redefined,
  Through loss, I found the design divine.
  So tell me, you reader, of shadows and flame,
  When a man loves, then rises again—
  Who is he, forged in love’s implosion?
  A broken file, or love’s new version?

  P.S. If all the official buttons are gone,
  build your own in the Attacker Lab and post straight to /send-valentine.
  -->

  <form method="POST">
    <div class="field">
      <input name="username" placeholder="username" />
    </div>
    <div class="field">
      <input name="password" type="password" placeholder="password" />
    </div>
    <button type="submit">Sign in</button>
  </form>

  {% if error %}
    <p class="error">{{ error }}</p>
  {% endif %}
  <p class="hint">
    Please sign in to send or receive Valentines.
    Username and Password is all lowercase. 
  </p>
</div>
</body>
</html>
"""

dashboard_tpl = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>HeartGram Dashboard</title>
  <style>
    * { box-sizing: border-box; }
    body {
      font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      margin: 0;
      min-height: 100vh;
      background:
        radial-gradient(circle at 0 0, #ffe4f3 0, #fff0f6 35%, #ffe4f3 70%, #fffafc 100%);
      color: #3b0b29;
    }
    .shell {
        max-width: 1180px;
        margin: 32px auto 40px;
        padding: 0 28px;
    }

    .topbar {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
      margin-bottom: 24px;
    }
    .brand {
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .brand-icon {
      width: 40px;
      height: 40px;
      border-radius: 14px;
      background: radial-gradient(circle at 30% 0, #fecaca, #fb7185);
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 10px 24px rgba(244, 63, 94, 0.38);
      font-size: 22px;
    }
    .brand-title {
      font-weight: 700;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      font-size: 14px;
      color: #be185d;
    }
    .chip-row {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      justify-content: flex-end;
    }
    .chip {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 5px 12px;
      border-radius: 999px;
      font-size: 11px;
      background: rgba(255, 255, 255, 0.9);
      border: 1px solid rgba(248, 187, 208, 0.9);
      color: #9f1239;
      text-decoration: none;
    }
    .chip strong {
      font-size: 12px;
    }
    .chip.primary {
      background: linear-gradient(135deg, #ec4899, #fb7185);
      border-color: transparent;
      color: #fff7fb;
      box-shadow: 0 10px 25px rgba(236, 72, 153, 0.55);
    }
    .chip.danger {
      border-color: #fb7185;
      color: #be123c;
    }
    .chip:hover {
      filter: brightness(1.03);
    }

    .grid {
    display: grid;
    grid-template-columns: minmax(0, 1.45fr) minmax(0, 1.1fr);
    gap: 24px;
    }


    @media (max-width: 900px) {
      .grid {
        grid-template-columns: minmax(0, 1fr);
      }
    }

    .panel {
      background: rgba(255, 255, 255, 0.95);
      border-radius: 24px;
      padding: 26px 26px 30px;
      box-shadow:
        0 22px 46px rgba(244, 114, 182, 0.38),
        0 0 0 1px rgba(252, 231, 243, 0.85);
      backdrop-filter: blur(18px);
      min-height: 260px;
    }
    .panel h1, .panel h2 {
      margin: 0 0 8px;
      font-size: 22px;
      color: #be185d;
    }
    .panel h1 span {
      font-size: 22px;
      margin-left: 4px;
    }
    .panel p {
      margin: 0 0 8px;
      font-size: 13px;
      line-height: 1.6;
      color: #4b1634;
    }
    .pill {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-size: 11px;
      padding: 3px 9px;
      border-radius: 999px;
      background: #fef2f2;
      color: #9f1239;
      border: 1px solid #fee2e2;
      margin-bottom: 4px;
    }
    .pill span {
      font-size: 13px;
    }

    .steps {
      margin-top: 10px;
      padding-left: 16px;
      font-size: 12px;
      color: #7f1d4b;
    }
    .steps li {
      margin-bottom: 4px;
    }

    .badge {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-size: 11px;
      padding: 3px 8px;
      border-radius: 999px;
      background: rgba(254, 242, 242, 0.95);
      color: #b91c1c;
      border: 1px dashed rgba(248, 113, 113, 0.8);
      margin-bottom: 6px;
    }

    textarea {
      width: 100%;
      border-radius: 14px;
      border: 1px solid #fecdd3;
      padding: 8px 10px;
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
      font-size: 13px;
      resize: vertical;
      background: #fff7fb;
      color: #4b1634;
    }
    textarea:focus {
      outline: none;
      border-color: #fb7185;
      box-shadow: 0 0 0 2px rgba(251, 113, 133, 0.25);
    }
    .bio-form textarea {
      min-height: 140px;
      background: #fff;
    }
    button {
      padding: 7px 14px;
      border-radius: 999px;
      border: none;
      background: linear-gradient(135deg, #ec4899, #fb7185);
      color: white;
      font-size: 13px;
      font-weight: 600;
      cursor: pointer;
      box-shadow: 0 10px 22px rgba(236, 72, 153, 0.5);
      display: inline-flex;
      align-items: center;
      gap: 6px;
      margin-top: 8px;
    }
    button span {
      font-size: 15px;
    }
    button:hover {
      filter: brightness(1.03);
      transform: translateY(-0.5px);
    }
    .bio-hint {
      font-size: 11px;
      color: #7f1d4b;
      margin-top: 6px;
    }
  </style>
</head>
<body>
  <div class="shell">
    <div class="topbar">
      <div class="brand">
        <div class="brand-icon">💘</div>
        <div>
          <div class="brand-title">HeartGram</div>
          <div style="font-size:11px;color:#7f1d4b;">
            Logged in as <strong>{{ user_name }}</strong> · ❤️ {{ hearts }} hearts
          </div>
        </div>
      </div>
      <div class="chip-row">
        <a class="chip" href="{{ url_for('profile', username=user_name) }}">My profile</a>
        <a class="chip" href="{{ url_for('profile', username='attacker') }}">Mysterious admirer</a>
        <a class="chip danger" href="{{ url_for('attacker_lab') }}">Attacker Lab</a>
        <a class="chip" href="{{ url_for('reset_hearts') }}">Reset hearts</a>
        <a class="chip primary" href="{{ url_for('logout') }}">Logout</a>
      </div>
    </div>

    <div class="grid">
      <div class="panel">
        <div class="pill"><span>🎯</span> Challenge</div>
        <h1>Today’s mission<span>💌</span></h1>
        <p>
          Cupid “removed” the official Valentine form, but the backend
          <code>/send-valentine</code> endpoint is still alive and trusting
          your browser a little too much.
        </p>
        <p>
          Somewhere on this site is a place where you can host your own HTML.
          Your goal is to make the victim’s browser send hearts from
          <code>victim</code> to <code>attacker</code>.
        </p>
        <ul class="steps">
          <li>Stay logged in as <code>victim</code>.</li>
          <li>Visit the <strong>Attacker Lab</strong> and craft a malicious form.</li>
        </ul>
      </div>

      <div class="panel">
        <div class="badge">CSRF Protected ✅</div>
        <h2>Edit your love bio</h2>
        <p>Not every form is vulnerable. This one actually checks a CSRF token.</p>
        <form class="bio-form" method="POST" action="{{ url_for('update_bio') }}">
          <input type="hidden" name="csrf_token" value="{{ csrf_token }}">
          <textarea name="bio">{{ bio }}</textarea>
          <button type="submit">
            Save bio
            <span>✨</span>
          </button>
          <div class="bio-hint">
            Hint: Compare this form’s protections to whatever you build in the Attacker Lab.
          </div>
        </form>
      </div>
    </div>
  </div>
</body>
</html>
"""

profile_tpl = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>{{ viewed_username }}'s Profile - HeartGram</title>
  <style>
    body { font-family: sans-serif; background: #fff0f6; margin: 0; }
    .container { width: 600px; margin: 40px auto; background: white;
                 padding: 20px; border-radius: 8px; box-shadow: 0 0 5px #f48fb1; }
    h1 { color: #ad1457; }
    pre { background: #fce4ec; padding: 10px; border-radius: 5px; overflow-x: auto; }
    .nav a { margin-right: 10px; color: #d81b60; text-decoration: none; }
  </style>
</head>
<body>
<div class="container">
  <div class="nav">
    <a href="{{ url_for('dashboard') }}">Back to dashboard</a>
  </div>
  <h1>@{{ viewed_username }}'s Valentine Profile</h1>
  <p>Hearts: ❤️ {{ hearts }}</p>
  <h3>Bio</h3>
  <p>{{ bio }}</p>

  {% if show_flag %}
    <h3>Secret admirer note</h3>
    <p>If you sent exactly the right number of hearts, here's your special flag:</p>
    <pre>{{ flag }}</pre>
  {% elif has_flag %}
    <p style="font-size: 12px; color: #555;">
      You can feel something special hidden here, but it is not meant for you yet.
    </p>
  {% endif %}
</div>
</body>
</html>
"""

attacker_lab_tpl = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Attacker Lab</title>
  <style>
    * { box-sizing: border-box; }
    body {
      margin: 0;
      min-height: 100vh;
      font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background:
        radial-gradient(circle at 0 0, #fee2f8 0, #fff0f6 40%, #ffe4f3 80%, #fffafd 100%);
      color: #3b0b29;
      display: flex;
      align-items: stretch;
      justify-content: center;
    }
    .shell {
      max-width: 1180px;
      width: 100%;
      margin: 32px auto 40px;
      padding: 0 28px;
    }
    .topbar {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
      margin-bottom: 20px;
    }
    .crumbs {
      font-size: 12px;
      color: #7f1d4b;
    }
    .crumbs a {
      color: #be123c;
      text-decoration: none;
    }
    .crumbs a:hover {
      text-decoration: underline;
    }
    .tag {
      padding: 4px 10px;
      border-radius: 999px;
      background: rgba(254, 242, 242, 0.95);
      border: 1px solid rgba(252, 165, 165, 0.9);
      font-size: 11px;
      color: #b91c1c;
      text-transform: uppercase;
      letter-spacing: 0.16em;
    }
    .layout {
      display: grid;
      grid-template-columns: minmax(0, 1.35fr) minmax(0, 1.1fr);
      gap: 22px;
    }
    @media (max-width: 880px) {
      .layout {
        grid-template-columns: minmax(0, 1fr);
      }
    }

    .panel {
      background: rgba(255, 255, 255, 0.96);
      border-radius: 24px;
      padding: 20px 20px 22px;
      box-shadow:
        0 22px 46px rgba(244, 114, 182, 0.38),
        0 0 0 1px rgba(252, 231, 243, 0.85);
      backdrop-filter: blur(18px);
      min-height: 460px;
    }
    h1 {
      margin: 4px 0 4px;
      font-size: 22px;
      color: #be185d;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .subtitle {
      margin: 0 0 10px;
      font-size: 13px;
      color: #4b1634;
    }
    .hint-block {
      background: #fff7fb;
      border-radius: 14px;
      padding: 8px 10px;
      border: 1px dashed #fecdd3;
      font-size: 12px;
      color: #7f1d4b;
      margin-bottom: 10px;
    }
    .hint-block code {
      background: #fee2f8;
      padding: 1px 4px;
      border-radius: 6px;
      font-size: 11px;
    }
    textarea {
      width: 100%;
      border-radius: 14px;
      border: 1px solid #fecdd3;
      padding: 8px 10px;
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
      font-size: 13px;
      resize: vertical;
      min-height: 220px;
      background: #fff;
      color: #4b1634;
    }
    textarea:focus {
      outline: none;
      border-color: #fb7185;
      box-shadow: 0 0 0 2px rgba(251, 113, 133, 0.25);
    }
    button {
      padding: 7px 16px;
      border-radius: 999px;
      border: none;
      background: linear-gradient(135deg, #ec4899, #fb7185);
      color: white;
      font-size: 13px;
      font-weight: 600;
      cursor: pointer;
      box-shadow: 0 10px 22px rgba(236, 72, 153, 0.5);
      display: inline-flex;
      align-items: center;
      gap: 6px;
      margin-top: 8px;
    }
    button span {
      font-size: 15px;
    }
    button:hover {
      filter: brightness(1.03);
      transform: translateY(-0.5px);
    }
    .small-note {
      font-size: 11px;
      color: #7f1d4b;
      margin-top: 6px;
    }

    .preview-panel h2 {
      margin: 0 0 6px;
      font-size: 15px;
      color: #be185d;
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .preview-box {
      margin-top: 6px;
      border-radius: 18px;
      background: #fff7fb;
      border: 1px solid #fecdd3;
      padding: 8px;
    }
    iframe {
        width: 100%;
        height: 420px;
        border-radius: 14px;
        border: none;
        background: white;
    }
  </style>
</head>
<body>
  <div class="shell">
    <div class="topbar">
      <div class="crumbs">
        <a href="{{ url_for('dashboard') }}">← Back to dashboard</a>
      </div>
    </div>

    <div class="layout">
      <div class="panel">
        <h1>Craft your spell 💌</h1>
        <p class="subtitle">
          Treat this like your own evil Valentine site. Any HTML you write here
          runs in the logged‑in victim’s browser and can send requests to
          HeartGram.
        </p>
        <div class="hint-block">
          <div style="margin-bottom:4px;"><strong>Hint:</strong> Build a form that:</div>
          <ul style="margin:0 0 4px 16px;padding:0;font-size:12px;">
            <li>uses <code>method="POST"</code></li>
            <li>targets <code>{{ target_url }}</code></li>
            <li>includes hidden fields <code>to</code>, <code>amount</code>, <code>message</code></li>
          </ul>
          <div>Give <code>attacker</code> <strong>exactly a certain number of hearts </strong> to reveal the flag.</div>
        </div>

        <form method="POST">
          <textarea name="html">{{ html|e }}</textarea>
          <button type="submit">
            Preview in victim browser
            <span>▶</span>
          </button>
          <div class="small-note">
            Example idea: a hidden form that auto‑submits or a friendly‑looking
            button that secretly posts to <code>/send-valentine</code>.
          </div>
        </form>
      </div>

      <div class="panel preview-panel">
        <h2>Live preview <span>👁️</span></h2>
        <p class="subtitle" style="margin-bottom:6px;">
          This frame shows exactly what the victim would see if they visited
          your malicious page while logged in.
        </p>
        <div class="preview-box">
          <iframe srcdoc="{{ html|e }}"></iframe>
        </div>
      </div>
    </div>
  </div>
</body>
</html>
"""

# ---------------- Helpers ----------------

def require_login():
    if "username" not in session:
        return redirect(url_for("login"))
    return None

# ---------------- Routes ----------------

@app.route("/")
def index():
    return render_template_string(index_tpl)

@app.route("/login", methods=["GET", "POST"])
def login():
    error = ""
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        user = users.get(username)
        if user and user["password"] == password:
            session["username"] = username
            session.setdefault("csrf_token", "fixed-token-for-demo")
            return redirect(url_for("dashboard"))
        else:
            error = "Love is not enough. Try again."
    return render_template_string(login_tpl, error=error)

@app.route("/dashboard")
def dashboard():
    r = require_login()
    if r:
        return r
    user = users[session["username"]]
    return render_template_string(
        dashboard_tpl,
        user_name=session["username"],
        hearts=user["hearts"],
        bio=user["bio"],
        csrf_token=session.get("csrf_token", "fixed-token-for-demo"),
    )

@app.route("/send-valentine", methods=["POST"])
def send_valentine():
    r = require_login()
    if r:
        return r
    sender_name = session["username"]
    sender = users[sender_name]

    to = request.form.get("to", "")
    amount = int(request.form.get("amount", "0") or 0)
    message = request.form.get("message", "")

    if to not in users:
        return "That heart does not know where to go.", 400
    if amount <= 0 or amount > sender["hearts"]:
        return "You cannot send that many hearts.", 400

    sender["hearts"] -= amount
    users[to]["hearts"] += amount

    print(f"[Valentine] {sender_name} sent {amount} hearts to {to}: {message}")
    return redirect(url_for("dashboard"))

@app.route("/update-bio", methods=["POST"])
def update_bio():
    r = require_login()
    if r:
        return r
    token = request.form.get("csrf_token")
    if token != session.get("csrf_token"):
        return "Your love letter looks forged (CSRF token invalid).", 403

    bio = request.form.get("bio", "")
    users[session["username"]]["bio"] = bio
    return redirect(url_for("dashboard"))

@app.route("/profile/<username>")
def profile(username):
    r = require_login()
    if r:
        return r
    if username not in users:
        return "No such lonely heart.", 404

    view = users[username]
    current_name = session["username"]

    show_flag = (
        view["flag"] is not None
        and current_name == "attacker"
        and view["hearts"] == 14
    )

    return render_template_string(
        profile_tpl,
        viewed_username=username,
        hearts=view["hearts"],
        bio=view["bio"],
        flag=view["flag"],
        show_flag=show_flag,
        has_flag=view["flag"] is not None,
    )

@app.route("/attacker-lab", methods=["GET", "POST"])
def attacker_lab():
    r = require_login()
    if r:
        return r
    html = ""
    if request.method == "POST":
        html = request.form.get("html", "")
    target_url = request.host_url.rstrip("/") + url_for("send_valentine")
    return render_template_string(attacker_lab_tpl, html=html, target_url=target_url)

@app.route("/reset-hearts")
def reset_hearts():
    users["victim"]["hearts"] = 100
    users["attacker"]["hearts"] = 0
    return redirect(url_for("dashboard"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# if __name__ == "__main__":

#     app.run(debug=True)


