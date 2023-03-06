import { faker } from "@faker-js/faker";
import prisma from "./client.js";
import {
  categoryList,
  usersList,
  entries,
  distributorList,
  exportsList,
} from "./data.js";

const generateFakeUsers = async (numFakeUsers) => {
  for (let index = 0; index < numFakeUsers; index++) {
    const firstName = faker.name.firstName();
    const lastName = faker.name.lastName();
    const email = faker.internet.email(firstName, lastName, "fakerjs.dev");
    await prisma.user.create({
      data: {
        email: email.toLowerCase(),
        name: `${firstName} ${lastName}`,
      },
    });
  }
};

const generateFakeData = async () => {
  // await prisma.user.deleteMany();
  // await generateFakeUsers(3);
  const userMap = new Map();
  const userSet = new Set();
  const createUsers = [];
  usersList.forEach((user) => {
    if (!userSet.has(user)) {
      createUsers.push({ name: user, email: user + "@gmail.com" });
      userSet.add(user);
    }
  });
  await prisma.user.createMany({ data: createUsers });
  const users = await prisma.user.findMany();
  users.forEach((user) => userMap.set(user.name, user));
  const createCats = [];
  const categoryMap = new Map();
  const categorySet = new Set();
  categoryList.forEach((category) => {
    if (!categorySet.has(category)) {
      createCats.push({ name: category, description: category });
      categorySet.add(category);
    }
  });
  await prisma.Category.createMany({ data: createCats });
  const categories = await prisma.Category.findMany();
  categories.forEach((category) => categoryMap.set(category.name, category));
  const createDistributors = [];
  const distributorMap = new Map();
  distributorList.forEach((distributor) =>
    createDistributors.push({ name: distributor })
  );
  await prisma.distributor.createMany({ data: createDistributors });
  const distributors = await prisma.distributor.findMany();
  distributors.forEach((dis) => distributorMap.set(dis.name, dis));
  const createEntryList = [];
  entries.forEach((entry) =>
    createEntryList.push({
      entryUserId: userMap.get(entry.name).id,
      inputDate: new Date(entry.date),
      weight: entry.weight,
      categoryIds: [categoryMap.get(entry.category).id],
      companyId: distributorMap.get(entry.distributor).id,
    })
  );
  const foodData = await prisma.pallot.createMany({ data: createEntryList });
  const createExportsList = [];
  exportsList.forEach((exportItem) =>
    createExportsList.push({
      userId: userMap.get(exportItem.name).id,
      exportDate: new Date(exportItem.date),
      weight: exportItem.weight,
      categoryId: categoryMap.get(exportItem.category).id,
      donatedTo: exportItem.donatedTo,
    })
  );
  const exports = await prisma.exports.createMany({ data: createExportsList });
};

try {
  generateFakeData();
} catch (err) {
  console.log(err);
  process.exit(1);
} finally {
  prisma.$disconnect();
}
