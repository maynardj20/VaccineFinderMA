[![mass-region-vaccine-check](https://github.com/maynardj20/VaccineFinderMA/actions/workflows/bos-sites-check.yml/badge.svg)](https://github.com/maynardj20/VaccineFinderMA/actions/workflows/bos-sites-check.yml)
# Massachusetts Region Covid 19 Vaccine Checker

This repository checks several CVS locations in the Massachusetts Region for availability of Covid 19 vaccination appointments.

Based on [VaccineFinderMA](https://github.com/JimmyAstle/VaccineFinderMA) by JimmyAstle, customized for locations I was curious about.

<!--start: status pages-->
**Last Updated**: 2021-04-17 07:50 AM

| Site                | Status         |
| ------------------- | -------------- |
| <img alt="" src="https://favicons.githubusercontent.com/www.cvs.com" height="13"> [CVS](https://www.cvs.com/immunizations/covid-19-vaccine)               | :no_entry: Unavailable    |
<!--end: status pages-->

## Site Information

This checks the following locations approximatly every 15 minutes using GitHub Actions.

* The following CVS locations:
  * Boston
  * Somerville
  * Dorchester
  * Brighton
  * Brookline
  * Cambridge
  * Medford
  * Arlington
  * Malden
  * Watertown
  * Waltham
  * Westford
  * Acton
  * Maynard
  * Concord
  * Leominster


## Historical data

Historical availability data from previous checks can be found in the [data/site-data.csv](data/site-data.csv) spreadsheet.

## Acknowledgements

The code in this repo is a forked version of the code found here [VaccineFinderMA](https://github.com/JimmyAstle/VaccineFinderMA), which is based on [CapitalRegionVaccine](https://github.com/CapitalRegionVaccine/CapitalRegionVaccine)

## 📄 License

- Code: [MIT](./LICENSE)
