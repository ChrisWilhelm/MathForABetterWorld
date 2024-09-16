import validate from "../util/checkValidation.js";
import prisma from "../../prisma/client.js";
import { StatusCodes } from "http-status-codes";

/**
 * Creates category
 * @param {object} req - request for the course
 * @param {object} res - response for the request
 */

export const createCategory = async (req, res) => {
  if (validate(req, res)) {
    return res;
  }
  const { name, description, isActive } = req.body;
  // const { id } = req.user;
  const category = await prisma.category.create({
    data: {
      name,
      description,
      isActive,
    },
  });
  return res.status(StatusCodes.CREATED).json({ category });
};

/**
 * READ a list of categories from the database
 * @param {object} req - request for the course
 * @param {object} res - response for the request
 */
export const getCategory = async (req, res) => {
  const category = await prisma.category.findMany();
  return res.status(StatusCodes.ACCEPTED).json({ category });
};

/**
 * UPDATE a category
 * @param {object} req - request for the course
 * @param {object} res - response for the request
 */
export const updateCategory = async (req, res) => {
  if (validate(req, res)) {
    return res;
  }
  const id = parseInt(req.params.id, 10);
  const { name, description, isActive } = req.body;
  const category = await prisma.category.update({
    where: {
      id,
    },
    data: {
      name,
      description,
      isActive,
    },
  });
  return res.status(StatusCodes.ACCEPTED).json({ category });
};

/**
 * DELETE a category
 * @param {object} req - request for the course
 * @param {object} res - response for the request
 */
export const deleteCategory = async (req, res) => {
  const id = parseInt(req.params.id, 10);
  const category = await prisma.category.delete({
    where: {
      id,
    },
  });
  return res.status(StatusCodes.ACCEPTED).json({ category });
};
