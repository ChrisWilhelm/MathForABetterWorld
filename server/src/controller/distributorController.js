import validate from "../util/checkValidation.js";
import prisma from "../../prisma/client.js";
import { StatusCodes } from "http-status-codes";

export const createDistributor = async (req, res) => {
  if (validate(req, res)) {
    return res;
  }
  const { name, isActive } = req.body;
  const distributor = await prisma.distributor.create({
    data: {
      name,
      isActive,
    },
  });
  return res.status(StatusCodes.CREATED).json({ distributor });
};

export const getDistributors = async (req, res) => {
  if (validate(req, res)) {
    return res;
  }
  const distributors = await prisma.distributor.findMany();
  return res.status(StatusCodes.ACCEPTED).json({ distributors });
};

export const deleteDistributor = async (req, res) => {
  if (validate(req, res)) {
    return res;
  }
  const id = parseInt(req.params.id, 10);
  const distributor = await prisma.distributor.delete({
    where: {
      id,
    },
  });
  return res.status(StatusCodes.ACCEPTED).json({ distributor });
};

export const updateDistributor = async (req, res) => {
  if (validate(req, res)) {
    return res;
  }
  const { id, name, isActive } = req.body;
  const distributor = await prisma.distributor.update({
    where: {
      id,
    },
    data: {
      name,
      isActive,
    },
  });
  return res.status(StatusCodes.ACCEPTED).json({ distributor });
};

export const getWeightsPerDistributor = async (req, res) => {
  if (validate(req, res)) {
    return res;
  }
  const distributors = await prisma.distributor.findMany({
    include: {
      distributedEntry: true,
    },
  });
  distributors.forEach((distributor) => {
    let sum = 0;
    distributor.distributedEntry.forEach((entry) => (sum += entry.weight));
    distributor["foodTotal"] = sum;
  });
  return res.status(StatusCodes.ACCEPTED).json({ distributors });
};
