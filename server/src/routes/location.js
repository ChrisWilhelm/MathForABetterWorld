import express from "express";
import { checkToken } from "../util/middleware.js";
import * as validator from "../util/locationMiddleware.js";
import * as controller from "../controller/locationController.js";
import * as express_validator from "express-validator";

const body = express_validator.body;
const param = express_validator.param;

const router = express.Router();
// Guide: https://www.prisma.io/docs/concepts/components/prisma-client/crud

router.post(
  "/",
  body("name", "Must include unique name for location").notEmpty(),
  body("longitude", "Longitude must be a string").notEmpty().isString(),
  body("latitude", "latitude must be a string").notEmpty().isString(),
  body("isActive", "isActive must be a boolean").notEmpty().isBoolean(),
  validator.isValidLatitude,
  validator.isValidLongitude,
  validator.isUniqueName,
  controller.createLocation
);

router.get("/", controller.getLocation);

router.delete(
  "/:id",
  param("id", "Must include id in the url params").notEmpty().isInt(),
  validator.isLocationId,
  controller.deleteLocation
);

router.post(
  "/:id/update",
  body("name", "Must include name in the request").notEmpty(),
  param("id", "Must include id in the body").notEmpty().isInt(),
  body("longitude", "Must include a string longitude in the body")
    .notEmpty()
    .isString(),
  body("latitude", "Must include a string latitude in the body")
    .notEmpty()
    .isString(),
  body("isActive", "isActive must be a boolean").notEmpty().isBoolean(),
  validator.isLocationId,
  validator.isUniqueNameNotId,
  controller.updateLocation
);

router.get("/visitsPerLocation", controller.getVisitsToLocation);

router.get("/weightPerLocation", controller.getWeightByLocation);

export default router;
