import validate from "../util/checkValidation.js";
import prisma from "../../prisma/client.js";
import { StatusCodes } from "http-status-codes";

/**
 * CREATE a rack
 * @param {object} req - request for the course
 * @param {object} res - response for the request
 */
export const createRack = async (req, res) => {
  if (validate(req, res)) {
    return res;
  }
  const { location, description, weightLimit, isActive } = req.body;
  // const { id } = req.user;
  const rack = await prisma.rack.create({
    data: {
      location,
      description,
      weightLimit,
      isActive,
    },
  });
  return res.status(StatusCodes.CREATED).json({ rack });
};

/**
 * READ a list of racks
 * @param {object} req - request for the course
 * @param {object} res - response for the request
 */
export const getRack = async (req, res) => {
  const rack = await prisma.rack.findMany();
  return res.status(StatusCodes.ACCEPTED).json({ rack });
};

/**
 * UPDATE a rack
 * @param {object} req - request for the course
 * @param {object} res - response for the request
 */
export const updateRack = async (req, res) => {
  if (validate(req, res)) {
    return res;
  }

  const id = parseInt(req.params.id, 10);
  const { location, description, weightLimit, isActive } = req.body;
  const rack = await prisma.rack.update({
    where: {
      id,
    },
    data: {
      location,
      description,
      weightLimit,
      isActive,
    },
  });
  return res.status(StatusCodes.ACCEPTED).json({ rack });
};

/**
 * DELETE a rack
 * @param {object} req - request for the course
 * @param {object} res - response for the request
 */
export const deleteRack = async (req, res) => {
  const id = parseInt(req.params.id, 10);
  const rack = await prisma.rack.delete({
    where: {
      id,
    },
  });
  return res.status(StatusCodes.ACCEPTED).json({ rack });
};
