import validate from "../util/checkValidation.js";
import prisma from "../../prisma/client.js";
import { StatusCodes } from "http-status-codes";

/**
 * Creates location
 * @param {object} req - request for the course
 * @param {object} res - response for the request
 */

export const createLocation = async (req, res) => {
  if (validate(req, res)) {
    return res;
  }
  const { name, longitude, latitude, isActive } = req.body;
  const location = await prisma.donationLocation.create({
    data: {
      name,
      longitude,
      latitude,
      isActive,
    },
  });
  return res.status(StatusCodes.CREATED).json({ location });
};

/**
 * READ a list of locations from the database
 * @param {object} req - request for the course
 * @param {object} res - response for the request
 */
export const getLocation = async (req, res) => {
  const location = await prisma.donationLocation.findMany();
  return res.status(StatusCodes.ACCEPTED).json({ location });
};

/**
 * UPDATE a location
 * @param {object} req - request for the course
 * @param {object} res - response for the request
 */
export const updateLocation = async (req, res) => {
  if (validate(req, res)) {
    return res;
  }
  const id = parseInt(req.params.id, 10);
  const { name, longitude, latitude, isActive } = req.body;
  const location = await prisma.donationLocation.update({
    where: {
      id,
    },
    data: {
      name,
      longitude,
      latitude,
      isActive,
    },
  });
  return res.status(StatusCodes.ACCEPTED).json({ location });
};

/**
 * DELETE a location
 * @param {object} req - request for the course
 * @param {object} res - response for the request
 */
export const deleteLocation = async (req, res) => {
  const id = parseInt(req.params.id, 10);
  const location = await prisma.donationLocation.delete({
    where: {
      id,
    },
  });
  return res.status(StatusCodes.ACCEPTED).json({ location });
};

/**
 * GET total visits to every location
 * @param {object} req - request for the course
 * @param {object} res - response for the request
 */
export const getVisitsToLocation = async (req, res) => {
  if (validate(req, res)) {
    return res;
  }
  const countOfVisits = await prisma.exportItem.groupBy({
    by: ["locationId"],
    _count: {
      exportDate: true,
    },
  });
  const locations = await prisma.donationLocation.findMany({});
  const countMap = new Map();
  countMap.set(null, null);
  locations.forEach((loc) => countMap.set(loc.id, loc));
  const countByLocation = [];
  countOfVisits.forEach((countVisit) => {
    countByLocation.push({
      count: countVisit._count.exportDate,
      locationId: countVisit.locationId,
      location: countMap.get(countVisit.locationId),
    });
  });
  return res.status(StatusCodes.OK).json({ countByLocation });
};

export const getWeightByLocation = async (req, res) => {
  if (validate(req, res)) {
    return res;
  }
  const countOfVisits = await prisma.exportItem.groupBy({
    by: ["locationId"],
    _sum: {
      weight: true,
    },
  });
  const locations = await prisma.donationLocation.findMany({});
  const countMap = new Map();
  countMap.set(null, null);
  locations.forEach((loc) => countMap.set(loc.id, loc));
  const countByLocation = [];
  countOfVisits.forEach((countVisit) => {
    countByLocation.push({
      sum: countVisit._sum.weight,
      locationId: countVisit.locationId,
      location: countMap.get(countVisit.locationId),
    });
  });
  return res.status(StatusCodes.OK).json({ countByLocation });
};
