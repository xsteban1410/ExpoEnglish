// What Linux are you? — cada respuesta suma puntos a una o varias distros; gana la que más tenga.

const DISTROS = {
  ubuntu: {
    name: "Ubuntu", family: "Debian family", url: "https://ubuntu.com",
    tagline: "Friendly, popular and ready for everything.",
    desc: "Ubuntu means \"humanity to others\". You like people, you like things that just work, and everybody knows you. Ubuntu is the most popular Linux for desktops.",
  },
  mint: {
    name: "Linux Mint", family: "Debian family", url: "https://linuxmint.com",
    tagline: "Calm, simple and comfortable.",
    desc: "You don't like complications. Linux Mint looks a bit like Windows, it is very easy to use, and it gives a second life to old computers.",
  },
  fedora: {
    name: "Fedora", family: "Red Hat family", url: "https://fedoraproject.org",
    tagline: "Modern, smart and curious.",
    desc: "You like new technology, but you want it to be well tested. Fedora is used by many programmers, and Linus Torvalds himself has used it.",
  },
  debian: {
    name: "Debian", family: "Debian family", url: "https://www.debian.org",
    tagline: "Stable, wise and reliable.",
    desc: "You are the person everybody trusts. Debian is one of the oldest distros (1993) and the base of Ubuntu and Mint. Slow changes, zero drama.",
  },
  arch: {
    name: "Arch Linux", family: "Arch family", url: "https://archlinux.org",
    tagline: "Independent, technical and always up to date.",
    desc: "You want to control everything and build your system piece by piece. Arch starts almost empty, and you decide what goes in. \"I use Arch, by the way.\"",
  },
  cachyos: {
    name: "CachyOS", family: "Arch family", url: "https://cachyos.org",
    tagline: "Fast, powerful and full of energy.",
    desc: "Speed is everything for you. CachyOS is based on Arch and optimized to get the maximum performance from your computer, especially for games.",
  },
  popos: {
    name: "Pop!_OS", family: "Debian family", url: "https://system76.com/pop",
    tagline: "Gamer, creative and productive.",
    desc: "You work hard and play hard. Pop!_OS is made by System76, a computer company, and it is great for games, graphics cards and getting things done.",
  },
  elementary: {
    name: "elementary OS", family: "Debian family", url: "https://elementary.io",
    tagline: "Elegant, artistic and calm.",
    desc: "You love beautiful, clean design. elementary OS looks a lot like macOS: simple, quiet and very pretty.",
  },
};

const QUESTIONS = [
  { q: "What is your computer like?", a: [
    ["💪", "New and very powerful", { cachyos: 2, arch: 1, popos: 1 }],
    ["🐢", "Old, but it still works", { mint: 2, debian: 2 }],
    ["💻", "A normal laptop", { ubuntu: 2, fedora: 1, elementary: 1 }],
    ["🎮", "A gaming PC with lights", { popos: 2, cachyos: 2 }],
  ] },
  { q: "What do you do most on the computer?", a: [
    ["🕹️", "Play video games", { cachyos: 2, popos: 2 }],
    ["📚", "Study and homework", { ubuntu: 2, mint: 1, elementary: 1 }],
    ["👩‍💻", "Programming", { fedora: 2, arch: 1, debian: 1 }],
    ["🎨", "Design, photos and music", { elementary: 2, ubuntu: 1, fedora: 1 }],
  ] },
  { q: "The terminal is…", a: [
    ["😅", "What is a terminal?", { mint: 2, elementary: 2 }],
    ["🙂", "OK, I can use it a little", { ubuntu: 2, popos: 1, fedora: 1 }],
    ["😎", "My favourite place", { arch: 2, debian: 1, cachyos: 1 }],
  ] },
  { q: "Choose a style for your desktop.", a: [
    ["🪟", "Classic, like Windows", { mint: 2, debian: 1 }],
    ["🍏", "Elegant, like a Mac", { elementary: 2, ubuntu: 1 }],
    ["✨", "Modern and clean", { fedora: 2, popos: 1, ubuntu: 1 }],
    ["🧩", "Minimal — I build it myself", { arch: 2, cachyos: 1 }],
  ] },
  { q: "How do you feel about updates?", a: [
    ["🛡️", "Never change something that works", { debian: 2, mint: 1 }],
    ["🧪", "New things, but well tested", { fedora: 2, ubuntu: 1, popos: 1 }],
    ["🚀", "I want the newest version today!", { arch: 2, cachyos: 2 }],
  ] },
  { q: "Your perfect weekend is…", a: [
    ["🍿", "A movie at home", { mint: 1, elementary: 2 }],
    ["🎧", "Video games with friends", { popos: 2, cachyos: 1 }],
    ["🔧", "Learning something new", { arch: 1, fedora: 1, debian: 1 }],
    ["🎉", "A party with lots of people", { ubuntu: 2 }],
  ] },
  { q: "Choose your motto.", a: [
    ["🌿", "Keep it simple", { mint: 2, elementary: 1 }],
    ["⚡", "Speed is everything", { cachyos: 2, arch: 1 }],
    ["🏛️", "Stability first", { debian: 2, mint: 1 }],
    ["✅", "Get things done", { popos: 2, fedora: 1, ubuntu: 1 }],
  ] },
  { q: "Pick an animal.", a: [
    ["🐢", "Turtle: slow and safe", { debian: 2 }],
    ["🐆", "Cheetah: super fast", { cachyos: 2, arch: 1 }],
    ["🐶", "Dog: friendly with everyone", { ubuntu: 2, mint: 1 }],
    ["🐱", "Cat: beautiful and independent", { elementary: 2, arch: 1 }],
    ["🦉", "Owl: smart and curious", { fedora: 2, popos: 1 }],
  ] },
];

// choices[i] = índice de respuesta de la pregunta i. Devuelve [[id, puntos], …] de mayor a menor;
// en empate gana el orden de DISTROS (estable).
function score(choices) {
  const pts = Object.fromEntries(Object.keys(DISTROS).map((k) => [k, 0]));
  choices.forEach((c, i) => {
    for (const [k, v] of Object.entries(QUESTIONS[i].a[c][2])) pts[k] += v;
  });
  return Object.entries(pts).sort((x, y) => y[1] - x[1]);
}

if (typeof module !== "undefined") module.exports = { DISTROS, QUESTIONS, score };

if (typeof document !== "undefined") {
  const $ = (id) => document.getElementById(id);
  const screens = ["intro", "quiz", "result"];
  let choices = [];

  const show = (id) => {
    screens.forEach((s) => { $(s).hidden = s !== id; });
    window.scrollTo(0, 0);
  };

  const render = () => {
    const i = choices.length;
    const item = QUESTIONS[i];
    $("counter").textContent = `Question ${i + 1} of ${QUESTIONS.length}`;
    $("question").textContent = item.q;
    $("bar").style.width = `${(i / QUESTIONS.length) * 100}%`;
    $("back").hidden = i === 0;
    $("answers").replaceChildren(...item.a.map(([emoji, text], j) => {
      const b = document.createElement("button");
      b.className = "answer";
      b.innerHTML = `<span class="emoji" aria-hidden="true">${emoji}</span><span></span>`;
      b.lastChild.textContent = text;
      b.onclick = () => {
        b.classList.add("selected");
        setTimeout(() => {
          choices.push(j);
          choices.length === QUESTIONS.length ? finish() : render();
        }, 180);
      };
      return b;
    }));
    $("answers").firstChild.focus({ preventScroll: true });
  };

  const finish = () => {
    const ranking = score(choices);
    const [top] = ranking[0];
    const d = DISTROS[top];
    const max = ranking[0][1] || 1;
    $("r-name").textContent = d.name;
    $("r-family").textContent = d.family;
    $("r-tagline").textContent = d.tagline;
    $("r-desc").textContent = d.desc;
    $("r-link").href = d.url;
    $("r-matches").replaceChildren(...ranking.slice(0, 3).map(([k, p]) => {
      const li = document.createElement("li");
      const pct = Math.round((p / max) * 100);
      li.innerHTML = `<div class="row"><span></span><span>${pct}%</span></div>
        <div class="track"><div class="fill" style="width:${pct}%"></div></div>`;
      li.querySelector("span").textContent = DISTROS[k].name;
      return li;
    }));
    show("result");
  };

  const start = () => { choices = []; show("quiz"); render(); };

  $("start").onclick = start;
  $("again").onclick = start;
  $("back").onclick = () => { choices.pop(); render(); };
  $("share").onclick = async () => {
    const text = `I am ${$("r-name").textContent}! What Linux are you?`;
    const url = location.href.split("#")[0];
    try {
      if (navigator.share) await navigator.share({ title: "What Linux are you?", text, url });
      else { await navigator.clipboard.writeText(`${text} ${url}`); $("share").textContent = "Copied!"; }
    } catch { /* el usuario canceló */ }
  };
}
