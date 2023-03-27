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
    const { name, longitude, latitude } = req.body;
    const category = await prisma.category.create({
      data: {
        name,
        longitude,
        latitude,
      },
    });
    return res.status(StatusCodes.CREATED).json({ category });
};

  /**
 * READ a list of locations from the database
 * @param {object} req - request for the course
 * @param {object} res - response for the request
 */
export const getLocation = async (req, res) => {
    const location = await prisma.location.findMany();
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
    const { name, longitude, latitude } = req.body;
    const location = await prisma.location.update({
      where: {
        id,
      },
      data: {
        name,
        longitude,
        latitude,
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
    const location = await prisma.location.delete({
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
    const countOfVisits = await prisma.user.groupBy({
        by: ['locationId'],
        _count: {
          exportDate: true,
        },
      })
    return res.status(StatusCodes.OK).json({ countOfVisits });
  };