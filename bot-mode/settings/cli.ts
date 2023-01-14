const [, , text] = process.argv;
import { BotInst } from "speedybot-mini";
import Bot from "./config";

const buildConfig = (BotRef, text: string) => {
  const botConfig = {
    token: "__",
    roomId: "",
    locales: { en: { greeting: ["hi!", "hello", "what's up"] } },
    SpeedybotInst: BotRef,
  };

  const trigger = {
    id: "id",
    authorId: "authorId",
    data: {
      id: "",
      roomId: "",
      roomType: "",
      text: "",
      personId: "",
      personEmail: "",
      html: "",
      mentionedPeople: [],
      created: new Date(),
      files: [],
    },
    author: {
      id: "",
      emails: [],
      phoneNumbers: [],
      displayName: "",
      nickName: "",
      userName: "",
      avatar: "",
      orgId: "",
      created: new Date(),
      status: "",
      type: "",
      firstName: "",
      lastName: "",
      lastModified: new Date(),
      lastActivity: new Date(),
    },
    text,
  };

  return {
    botConfig,
    trigger,
  };
};
async function main(text: string) {
  const handler = Bot.processText(text);

  if (handler) {
    const { botConfig, trigger } = buildConfig(Bot, text);
    const res = await handler(new BotInst(botConfig), trigger);
    console.log(res); // communicate via stdout?
  }
}
main(text);
