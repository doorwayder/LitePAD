"use strict";

function date_today() {
    const time1 = document.getElementById("startdate")
    const time2 = document.getElementById("stopdate")
    const form = document.getElementById("mainform");
    time1.valueAsDate = new Date();
    time2.valueAsDate = new Date();
    form.submit();
}


function date_yesterday() {
    const time1 = document.getElementById("startdate")
    const time2 = document.getElementById("stopdate")
    const form = document.getElementById("mainform");
    let date = new Date();
    date.setDate(date.getDate() - 1);
    time1.valueAsDate = date;
    time2.valueAsDate = date;
    form.submit();
}


function date_beforeyesterday() {
    const time1 = document.getElementById("startdate")
    const time2 = document.getElementById("stopdate")
    const form = document.getElementById("mainform");
    let date = new Date();
    date.setDate(date.getDate() - 2);
    time1.valueAsDate = date;
    time2.valueAsDate = date;
    form.submit();
}


function date_week() {
    const time1 = document.getElementById("startdate")
    const time2 = document.getElementById("stopdate")
    const form = document.getElementById("mainform");
    let date = new Date();
    time2.valueAsDate = date;
    date.setDate(date.getDate() - 7);
    time1.valueAsDate = date;
    form.submit();
}


function date_month() {
    const time1 = document.getElementById("startdate")
    const time2 = document.getElementById("stopdate")
    const form = document.getElementById("mainform");
    let date = new Date();
    time2.valueAsDate = date;
    date.setDate(1);
    time1.valueAsDate = date;
    form.submit();
}


function date_custom() {
    const form = document.getElementById("mainform");
    form.submit();
}
