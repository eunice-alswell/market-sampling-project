CREATE TABLE "SamplingTable" (
  "samplingID" int UNIQUE PRIMARY KEY,
  "samplingDate" date,
  "areaID" int,
  "SamplingTypeID" int,
  "InstitutionTypeID" int,
  "PromoterID" int,
  "SamplingTarget" int,
  "SamplingCount" int,
  "PassengersPerCar" int
);

CREATE TABLE "Area" (
  "areaID" int UNIQUE PRIMARY KEY,
  "areaName" varchar,
  "district" varchar,
  "Region" varchar
);

CREATE TABLE "SamplingTypeTable" (
  "SamplingTypeID" int UNIQUE PRIMARY KEY,
  "SamplingTypeName" varchar
);

CREATE TABLE "InstitutionTypeTable" (
  "InstitutionTypeID" int UNIQUE PRIMARY KEY,
  "InstitutionName" varchar
);

CREATE TABLE "PromoterTable" (
  "PromoterID" int UNIQUE PRIMARY KEY,
  "Name" varchar,
  "Contact" varchar
);

CREATE TABLE "RespondentTable" (
  "respondentID" int UNIQUE PRIMARY KEY,
  "samplingID" int UNIQUE,
  "fullName" varchar,
  "ageRange" varchar,
  "contact" varchar,
  "residenceArea" varchar,
  "preferredBrand" varchar,
  "reason" varchar,
  "optInOtherProducts" varchar,
  "Dateofsubmission" datetime
);

CREATE TABLE "Date" (
  "ActualDate" "Date" UNIQUE,
  "day" date,
  "week" date,
  "month" date,
  "year" date
);

ALTER TABLE "SamplingTable" ADD FOREIGN KEY ("areaID") REFERENCES "Area" ("areaID");

ALTER TABLE "SamplingTable" ADD FOREIGN KEY ("SamplingTypeID") REFERENCES "SamplingTypeTable" ("SamplingTypeID");

ALTER TABLE "SamplingTable" ADD FOREIGN KEY ("InstitutionTypeID") REFERENCES "InstitutionTypeTable" ("InstitutionTypeID");

ALTER TABLE "SamplingTable" ADD FOREIGN KEY ("PromoterID") REFERENCES "PromoterTable" ("PromoterID");

ALTER TABLE "RespondentTable" ADD FOREIGN KEY ("samplingID") REFERENCES "SamplingTable" ("samplingID");

ALTER TABLE "Date" ADD FOREIGN KEY ("ActualDate") REFERENCES "SamplingTable" ("samplingDate");

ALTER TABLE "Date" ADD FOREIGN KEY ("ActualDate") REFERENCES "RespondentTable" ("Dateofsubmission");
