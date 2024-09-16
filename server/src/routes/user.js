import express from "express";
import * as express_validator from "express-validator";
import * as validator from "../util/userMiddleware.js";
import * as controller from "../controller/userController.js";

const body = express_validator.body;
const param = express_validator.param;

const router = express.Router();
// Here the routes will be listed with correspodning middleware

// Example routes from another app:
router.post(
  "/signup",
  body("email", "Email is required").notEmpty().isEmail(),
  body("name", "Name is required").notEmpty(),
  body("phoneNumber", "Phone number must be a string").optional().isString(),
  body("address", "Address must be a string").optional().isString(),
  body("isActive", "isActive must be a boolean").notEmpty().isBoolean(),
  validator.isUniqueEmail,
  validator.isUniquePhoneNumber,
  controller.create
);

router.get("/", controller.get);

router.get(
  "/userWhoWorkedTheMostHours",
  controller.getUserWhoWorkedTheMostHours
);

router.post(
  "/update",
  body("email", "Email is required").notEmpty().isEmail(),
  body("id", "Id is required").notEmpty().isInt(),
  body("phoneNumber", "Phone number must be a string").optional().isString(),
  body("address", "Address must be a string").optional().isString(),
  body("isActive", "isActive must be a boolean").notEmpty().isBoolean(),
  validator.isUniqueEmail,
  validator.isUniquePhoneNumber,
  controller.update
);

// get total number of hours worked accross all volunteers
router.get("/totalUserHours", controller.getTotalUserHours);
export default router;
