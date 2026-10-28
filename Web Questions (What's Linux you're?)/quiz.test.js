// node --test quiz.test.js — cada distro debe poder ganar y ninguna debe dominar.
const test = require("node:test");
const assert = require("node:assert");
const { DISTROS, QUESTIONS, score } = require("./quiz.js");

test("todas las distros pueden ganar con un reparto razonable", () => {
  const wins = Object.fromEntries(Object.keys(DISTROS).map((k) => [k, 0]));
  let total = 0;
  const walk = (choices) => {
    if (choices.length === QUESTIONS.length) { wins[score(choices)[0][0]]++; total++; return; }
    QUESTIONS[choices.length].a.forEach((_, j) => walk([...choices, j]));
  };
  walk([]);
  console.log(Object.fromEntries(Object.entries(wins).map(([k, v]) => [k, `${(100 * v / total).toFixed(1)}%`])));
  for (const [k, v] of Object.entries(wins)) {
    assert.ok(v / total > 0.03, `${k} casi nunca gana`);
    assert.ok(v / total < 0.30, `${k} gana demasiado`);
  }
});
