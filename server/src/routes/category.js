import express from "express";
import { checkToken } from "../util/middleware.js";
import * as validator from "../util/categoryMiddleware.js";
import * as controller from "../controller/categoryController.js";
import * as express_validator from "express-validator";

const body = express_validator.body;
const param = express_validator.param;

const router = express.Router();
// Guide: https://www.prisma.io/docs/concepts/components/prisma-client/crud

router.post(
  "/",
  body("name", "Must include unique name for category").notEmpty(),
  body("description", "Description must be a string").notEmpty().isString(),
  body("isActive", "isActive must be a boolean").notEmpty().isBoolean(),
  validator.isUniqueName,
  controller.createCategory
);

router.get("/", controller.getCategory);

router.delete(
  "/:id",
  param("id", "Must include id in the url params").notEmpty().isInt(),
  validator.isCategoryId,
  controller.deleteCategory
);

router.post(
  "/:id/update",
  body("name", "Must include name in the request").notEmpty(),
  param("id", "Must include id in the body").notEmpty().isInt(),
  body("description", "Must include a string description in the body")
    .notEmpty()
    .isString(),
  body("isActive", "isActive must be a boolean").notEmpty().isBoolean(),
  validator.isCategoryId,
  validator.isUniqueNameNotId,
  controller.updateCategory
);

export default router;
