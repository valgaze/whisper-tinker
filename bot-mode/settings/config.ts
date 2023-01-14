import { Speedybot, Config } from "speedybot-mini";
import "cross-fetch/polyfill";

const botConfig: Config = {
  locales: {
    es: {
      greetings: {
        welcome: "hola!!",
      },
    },
    cn: {
      greetings: {
        welcome: "你好",
      },
    },
  },
};

// In a production environment use a secrets manager to pass in token

// 1) Initialize your bot w/ config
const MyBot = new Speedybot(botConfig);

// 2) Export your bot
export default MyBot;

// 3) Do whatever you want!
MyBot.nlu(async ($bot, msg) => {
  $bot.log(`This text was transmitted: ${msg.text}`);
});

MyBot.noMatch(($bot) => {
  $bot.log("heatless...");
  return Math.random() as unknown as void;
});

MyBot.contains(["ping", "pong"], ($bot, msg) => {
  const { text } = msg;
  if (text === "ping") {
    const returnVal = "pong" as unknown as void; // fix
    $bot.log("pong");
    return returnVal;
  } else if (text === "pong") {
    const returnVal = "ping" as unknown as void; // fix
    $bot.log("ping");
    return returnVal;
  }
});

MyBot.exact("locale", ($bot) => {
  const returnVal = $bot.translate("cn", "greetings.welcome");
  $bot.log($bot.translate("cn", "greetings.welcome"));
  $bot.log($bot.translate("es", "greetings.welcome"));
  return returnVal;
});

MyBot.fuzzy(["help", "how do i"], ($bot, msg) => {
  const res = `Just say bongo help me` as unknown as void;
  $bot.log(res);
  return res;
});
