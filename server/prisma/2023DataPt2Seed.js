import { faker } from "@faker-js/faker";
import prisma from "./client.js";
import { Role } from "@prisma/client";
import { hashPassword } from "../src/util/password.js";

import {
  volunteers,
  imports,
  exports,
  distributorsList,
} from "./2023DataPt2.js";

const generateFakeData = async () => {
  // await prisma.user.deleteMany();
  // await generateFakeUsers(3);
  const existingLocationsSet = new Set();
  const existingLocations = await prisma.donationLocation.findMany();
  existingLocations.forEach((loc) =>
    existingLocationsSet.add(loc.name.toLowerCase())
  );
  const locationsToAdd = [];
  exports.forEach((exp) => {
    if (!existingLocationsSet.has(exp.location.toLowerCase())) {
      locationsToAdd.push({
        name: exp.location,
        latitude: "0",
        longitude: "0",
      });
    }
  });
  await prisma.donationLocation.createMany({ data: locationsToAdd });

  const locationMap = new Map();
  const locations = await prisma.donationLocation.findMany();
  locations.forEach((loc) => locationMap.set(loc.name.toLowerCase(), loc));
  const userMap = new Map();
  const existingUsers = await prisma.user.findMany();
  existingUsers.forEach((user) => userMap.set(user.name.toLowerCase(), user));
  const categoryMap = new Map();
  const categories = await prisma.category.findMany();
  categories.forEach((category) =>
    categoryMap.set(category.name.toLowerCase(), category)
  );
  const createDistributors = [];
  const existingDistributors = await prisma.distributor.findMany();
  const existingDistributorsMap = new Map();

  existingDistributors.forEach((dis) =>
    existingDistributorsMap.set(dis.name.toLowerCase(), dis)
  );
  const distributorMap = new Map();
  distributorsList.forEach((distributor) => {
    if (!existingDistributorsMap.has(distributor.toLowerCase())) {
      createDistributors.push({ name: distributor });
    }
  });
  await prisma.distributor.createMany({ data: createDistributors });
  const distributors = await prisma.distributor.findMany();
  distributors.forEach((dis) =>
    distributorMap.set(dis.name.toLowerCase(), dis)
  );
  const rackMap = new Map();
  const racks = await prisma.rack.findMany();
  racks.forEach((rack) => rackMap.set(rack.location.toLowerCase(), rack));

  // Collect users to be created from volunteerList
  const newUsers = [];
  const userSet = new Set();
  volunteers.forEach((entry) => {
    if (
      !userMap.has(entry.name.toLowerCase()) &&
      !userSet.has(entry.name.toLowerCase())
    ) {
      newUsers.push({
        name: entry.name,
        email: entry.name.replace(/\s+/g, "") + "@gmail.com",
      });
      userSet.add(entry.name.toLowerCase());
    }
  });

  imports.forEach((entry) => {
    if (
      !userMap.has(entry.name.toLowerCase()) &&
      !userSet.has(entry.name.toLowerCase())
    ) {
      newUsers.push({
        name: entry.name,
        email: entry.name.replace(/\s+/g, "") + "@gmail.com",
      });
      userSet.add(entry.name.toLowerCase());
    }
  });

  exports.forEach((entry) => {
    if (
      !userMap.has(entry.name.toLowerCase()) &&
      !userSet.has(entry.name.toLowerCase())
    ) {
      newUsers.push({
        name: entry.name,
        email: entry.name.replace(/\s+/g, "") + "@gmail.com",
      });
      userSet.add(entry.name.toLowerCase());
    }
  });

  // Create new users in bulk
  if (newUsers.length > 0) {
    const createdUsers = await prisma.user.createMany({ data: newUsers });
    const updatedUsers = await prisma.user.findMany({
      where: {
        name: {
          in: newUsers.map((u) => u.name),
        },
      },
    });
    updatedUsers.forEach((user) => userMap.set(user.name.toLowerCase(), user));
  }

  const createEntryList = [];
  imports.forEach((entry) => {
    console.log(entry);
    if (rackMap.has(entry.rack)) {
      createEntryList.push({
        entryUserId: userMap.get(entry.name.toLowerCase()).id,
        inputDate: new Date(entry.date),
        weight: entry.weight,
        categoryIds: [categoryMap.get(entry.category.toLowerCase()).id],
        companyId: distributorMap.get(entry.distributor.toLowerCase()).id,
        rackId: rackMap.get(entry.rack).id,
      });
    } else {
      createEntryList.push({
        entryUserId: userMap.get(entry.name.toLowerCase()).id,
        inputDate: new Date(entry.date),
        weight: entry.weight,
        categoryIds: categoryMap.get(entry.category.toLowerCase()).id,
        companyId: distributorMap.get(entry.distributor.toLowerCase()).id,
      });
    }
  });
  await prisma.pallet.createMany({ data: createEntryList });
  const createExportsList = [];
  exports.forEach((exportItem) => {
    let exportType = "Regular";

    if (exportItem.weight < 0) {
      exportType = "Return";
    }
    console.log(exportItem);
    if (rackMap.has(exportItem.rack)) {
      createExportsList.push({
        userId: userMap.get(exportItem.name.toLowerCase()).id,
        exportDate: new Date(exportItem.date.toLowerCase()),
        weight: exportItem.weight,
        categoryId: categoryMap.get(exportItem.category.toLowerCase()).id,
        locationId: locationMap.get(exportItem.location.toLowerCase()).id,
        rackId: rackMap.get(exportItem.rack.toLowerCase()).id,
        exportType: exportType,
      });
    } else {
      createExportsList.push({
        userId: userMap.get(exportItem.name.toLowerCase()).id,
        exportDate: new Date(exportItem.date),
        weight: exportItem.weight,
        categoryId: categoryMap.get(exportItem.category.toLowerCase()).id,
        locationId: locationMap.get(exportItem.location.toLowerCase()).id,
        exportType: exportType,
      });
    }
  });
  await prisma.exportItem.createMany({
    data: createExportsList,
  });
  const createShiftList = [];
  volunteers.forEach((entry) => {
    createShiftList.push({
      userId: userMap.get(entry.name.toLowerCase()).id,
      start: new Date(entry.start),
      end: new Date(entry.end),
      regularFoodTaken: entry.regularTaken,
      damagedFoodTaken: entry.damagedTaken,
    });
  });
  await prisma.shift.createMany({ data: createShiftList });
};

try {
  generateFakeData();
} catch (err) {
  console.log(err);
  process.exit(1);
} finally {
  prisma.$disconnect();
}