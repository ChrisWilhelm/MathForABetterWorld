import validate from "../util/checkValidation.js";
import prisma from "../../prisma/client.js";
import { StatusCodes } from "http-status-codes";

/**
 * CREATE a shift
 * @param {object} req - request for the course
 * @param {object} res - response for the request
 */
export const createShift = async (req, res) => {
  if (validate(req, res)) {
    return res;
  }
  const { userId, start, end, regularFoodTaken, damagedFoodTaken } = req.body;
  // const { id } = req.user;
  const shift = await prisma.shift.create({
    data: {
      userId,
      start: new Date(start),
      end: end !== "1970-01-01T00:00:00.000Z" ? new Date(end) : null,
      regularFoodTaken,
      damagedFoodTaken,
    },
  });
  return res.status(StatusCodes.CREATED).json({ shift });
};

/**
 * READ a list of shifts
 * @param {object} req - request for the course
 * @param {object} res - response for the request
 */
export const getShift = async (req, res) => {
  const shift = await prisma.shift.findMany();
  return res.status(StatusCodes.ACCEPTED).json({ shift });
};

/**
 * UPDATE a shift
 * @param {object} req - request for the course
 * @param {object} res - response for the request
 */
export const updateShift = async (req, res) => {
  if (validate(req, res)) {
    return res;
  }

  const { id, user, userId, start, end, regularFoodTaken, damagedFoodTaken } =
    req.body;
  const shift = await prisma.shift.update({
    where: {
      id,
    },
    data: {
      userId,
      start,
      end,
      regularFoodTaken,
      damagedFoodTaken,
    },
  });
  return res.status(StatusCodes.ACCEPTED).json({ shift });
};

/**
 * DELETE a shift
 * @param {object} req - request for the course
 * @param {object} res - response for the request
 */
export const deleteShift = async (req, res) => {
  const id = parseInt(req.params.id, 10);
  const shift = await prisma.shift.delete({
    where: {
      id,
    },
  });
  return res.status(StatusCodes.ACCEPTED).json({ shift });
};

/**
 * Gets total volunteer hours worked accross all shifts
 * @param {object} req - request for the course
 * @param {object} res - response for the request
 */
export const getTotalHoursWorked = async (req, res) => {
  if (validate(req, res)) {
    return res;
  }
  const totalHours = await prisma.shift.aggregate({
    _sum: {
      duration: {
        _divide: [
          { _subtract: ["end", "start"] }, // subtract outputs time in milliseconds
          3600000, // convert milliseconds to hours
        ],
      },
    },
  });
  return res.status(StatusCodes.OK).json({ totalHours }); // changed to OK status code?
};

export const signout = async (req, res) => {
  if (validate(req, res)) {
    return res;
  }
  const { id, regularFoodTaken, damagedFoodTaken } = req.body;
  const end = new Date();
  const startShift = await prisma.shift.findUnique({ where: { id } });
  const duration = Math.round((end - startShift.start) / 60000);
  const shift = await prisma.shift.update({
    where: {
      id,
    },
    data: {
      end,
      regularFoodTaken,
      damagedFoodTaken,
      duration,
    },
  });
  return res.status(StatusCodes.ACCEPTED).json({ shift });
};

export const getActiveShifts = async (req, res) => {
  if (validate(req, res)) {
    return res;
  }
  const activeShifts = await prisma.shift.findMany({
    where: {
      OR: [
        {
          end: null,
        },
        {
          end: "1970-01-01T00:00:00.000Z",
        },
      ],
    },
    include: {
      user: true,
    },
  });
  return res.status(StatusCodes.ACCEPTED).json({ activeShifts });
};

export const getTotalFoodGivenToVolunteers = async (req, res) => {
  if (validate(req, res)) {
    return res;
  }
  const totalRegularFoodToVolunteers = await prisma.shift.aggregate({
    _sum: {
      regularFoodTaken: true,
    },
  });
  const totalDamagedFoodToVolunteers = await prisma.shift.aggregate({
    _sum: {
      damagedFoodTaken: true,
    },
  });
  return res
    .status(StatusCodes.ACCEPTED)
    .json({ totalRegularFoodToVolunteers, totalDamagedFoodToVolunteers });
};

export const getShiftsInRange = async (req, res) => {
  if (validate(req, res)) {
    return res;
  }
  const { startDate, endDate } = req.params;
  const startObj = new Date(startDate);
  const endObj = new Date(endDate);
  const shifts = await prisma.shift.findMany({
    where: {
      AND: [
        {
          start: {
            lte: endObj,
          },
        },
        {
          start: {
            gte: startObj,
          },
        },
      ],
    },
  });
  return res.status(StatusCodes.ACCEPTED).json({ shifts });
};
