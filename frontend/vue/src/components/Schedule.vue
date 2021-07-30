<template >
  <div :key="componentKey">
  <input type="hidden" id="customer" :value=this.$route.params.id>
   <div id="menu">
      <span id="menu-navi">
        <button type="button" class="btn btn-default btn-sm move-today" data-action="move-today">Today</button>
        <button type="button" class="btn btn-default btn-sm move-day" data-action="move-prev">
          <i class="calendar-icon ic-arrow-line-left" data-action="move-prev"></i>
        </button>
        <button type="button" class="btn btn-default btn-sm move-day" data-action="move-next">
          <i class="calendar-icon ic-arrow-line-right" data-action="move-next"></i>
        </button>
      </span>
      <span id="renderRange" class="render-range"></span>
    <span style="margin-left:20px;"><button id="commit" class="btn btn-dark" type="button" v-on:click="componentKey++" disabled>Commit to this booking</button></span>
    </div>
    <div id="calendar" style="top:400px;"></div>
  </div>

</template>

<script>
import '../css/bootstrap.css';
import 'tui-time-picker/dist/tui-time-picker.css';
import 'tui-date-picker/dist/tui-date-picker.css';
import 'tui-calendar/dist/tui-calendar.min.css';
import '../css/default.css';
import '../css/icons.css';

import '../js/bootstrap.min';
//import 'tui-code-snippet';
import 'tui-time-picker'
import 'tui-date-picker'
import moment from 'moment'
import 'chance'
import Calendar from 'tui-calendar'

export default {
  name: 'Schedule',

  methods: {
      forceRerender(){
        this.componentKey += 1;  
      }
  },data() {
      return{ componentKey: 0};
    },

  mounted: function () {   
   var guid = '';
   var CalendarList = [];
    function CalendarInfo() {
        this.id = null;
        this.name = null;
        this.checked = true;
        this.color = null;
        this.bgColor = null;
        this.borderColor = null;
    }
    function addCalendar(calendar) {
        CalendarList.push(calendar);
    }
    function findCalendar(id) {
        var found;
        CalendarList.forEach(function(calendar) {
            if (calendar.id === id) {
                found = calendar;
            }
        });
        return found;
    }
    function hexToRGBA(hex) {
        var radix = 16;
        var r = parseInt(hex.slice(1, 3), radix),
            g = parseInt(hex.slice(3, 5), radix),
            b = parseInt(hex.slice(5, 7), radix),
            a = parseInt(hex.slice(7, 9), radix) / 255 || 1;
        var rgba = 'rgba(' + r + ', ' + g + ', ' + b + ', ' + a + ')';
        return rgba;
    }
    (function() {
        var calendar;
        var id = 0;
        calendar = new CalendarInfo();
        id += 1;
        calendar.id = String(id);
        calendar.name = 'Bookings';
        calendar.color = '#ffffff';
        calendar.bgColor = '#9e5fff';
        calendar.dragBgColor = '#9e5fff';
        calendar.borderColor = '#9e5fff';
        addCalendar(calendar);
    })();
    /**/
    var ScheduleList = [];
    var SCHEDULE_CATEGORY = [
        'milestone',
        'task'
    ];
    function ScheduleInfo() {
        this.id = null;
        this.calendarId = null;
        this.title = null;
        this.isAllday = false;
        this.start = null;
        this.end = null;
        this.category = '';
        this.dueDateClass = '';
        this.color = null;
        this.bgColor = null;
        this.dragBgColor = null;
        this.borderColor = null;
        this.customStyle = '';
        this.isFocused = false;
        this.isPending = false;
        this.isVisible = true;
        this.isReadOnly = false;
        this.raw = {
            memo: '',
            hasToOrCc: false,
            hasRecurrenceRule: false,
            location: null,
            class: 'public', // or 'private'
            creator: {
                name: '',
                avatar: '',
                company: '',
                email: '',
                phone: ''
            }
        };
    }
    function generateTime(schedule, renderStart, renderEnd) {
        var baseDate = new Date(renderStart);
        var singleday = chance.bool({likelihood: 70});
        var startDate = moment(renderStart.getTime())
        var endDate = moment(renderEnd.getTime());
        var diffDate = endDate.diff(startDate, 'days');
        schedule.isAllday = chance.bool({likelihood: 30});
        if (schedule.isAllday) {
            schedule.category = 'allday';
        } else if (chance.bool({likelihood: 30})) {
            schedule.category = SCHEDULE_CATEGORY[chance.integer({min: 0, max: 1})];
            if (schedule.category === SCHEDULE_CATEGORY[1]) {
                schedule.dueDateClass = 'morning';
            }
        } else {
            schedule.category = 'time';
        }
        startDate.add(chance.integer({min: 0, max: diffDate}), 'days');
        startDate.hours(chance.integer({min: 0, max: 23}))
        startDate.minutes(chance.bool() ? 0 : 30);
        schedule.start = startDate.toDate();
        endDate = moment(startDate);
        if (schedule.isAllday) {
            endDate.add(chance.integer({min: 0, max: 3}), 'days');
        }
        schedule.end = endDate
            .add(chance.integer({min: 1, max: 4}), 'hour')
            .toDate();
    }
    /**/
      var cal, resizeThrottled;
      var useCreationPopup = false;
      var useDetailPopup = true;
      var datePicker, selectedCalendar;
      cal = new Calendar('#calendar', {
          defaultView: 'week',
          useCreationPopup: useCreationPopup,
          useDetailPopup: useDetailPopup,
          calendars: CalendarList,
          scheduleView: ['time'],
          taskView: false,
          template: {
              time: function(schedule) {
                  return getTimeTemplate(schedule, false);
              },
            }
      });

      cal.setOptions({
        week: {
            hourStart: 8,
            hourEnd: 19,
            workweek: true
        }
        });

      // event handlers
      cal.on({
          'clickSchedule': function(e) {
              console.log('clickSchedule', e);
              $("button.tui-full-calendar-popup-edit").hide();
          },
          'clickDayname': function(date) {
              console.log('clickDayname', date);
          },
          'beforeCreateSchedule': function(e) {
              console.log('beforeCreateSchedule', e);
              var start = e.start;
              var now = new Date();
              if (start > now)
              {
              saveNewSchedule(e);
              } else {
                  alert("Can't book in the past.");
                  }
          },
          'beforeDeleteSchedule': function(e) {
              console.log('beforeDeleteSchedule', e);
              cal.deleteSchedule(e.schedule.id, e.schedule.calendarId);
              $("button#commit").prop('disabled', true);
              while (ScheduleList.length > 0) {
                    ScheduleList.pop();
                }
          },
          'afterRenderSchedule': function(e) {
              var schedule = e.schedule;
          }
      });
      /**
       * Get time template for time and all-day
       * @param {Schedule} schedule - schedule
       * @param {boolean} isAllDay - isAllDay or hasMultiDates
       * @returns {string}
       */
      function getTimeTemplate(schedule, isAllDay) {
          var html = [];
          var start = moment(schedule.start.toUTCString());
          if (!isAllDay) {
              html.push('<strong>' + start.format('HH:mm') + '</strong> ');
          }
          if (schedule.isPrivate) {
              html.push('<span class="calendar-font-icon ic-lock-b"></span>');
              html.push(' Private');
          } else {
              if (schedule.isReadOnly) {
                  html.push('<span class="calendar-font-icon ic-readonly-b"></span>');
              } else if (schedule.recurrenceRule) {
                  html.push('<span class="calendar-font-icon ic-repeat-b"></span>');
              } else if (schedule.attendees.length) {
                  html.push('<span class="calendar-font-icon ic-user-b"></span>');
              } else if (schedule.location) {
                  html.push('<span class="calendar-font-icon ic-location-b"></span>');
              }
              html.push(' ' + schedule.title);
          }
          return html.join('');
      }
      function onClickNavi(e) {
          var action = getDataAction(e.target);
          switch (action) {
              case 'move-prev':
                  cal.prev();
                  break;
              case 'move-next':
                  cal.next();
                  break;
              case 'move-today':
                  cal.today();
                  break;
              default:
                  return;
          }
          setRenderRangeText();
          setSchedules();
          fetchSchedules();
      }

    function fetchSchedules(){
        console.log("fetching schedules");
        var range = $("span#renderRange").text().split('~');
        var start = range[0].replaceAll('.', '-').trim();
        var end = start.split('-')[0]+"-"+(range[1].replaceAll('.','-').trim());
        $.get("http://localhost:8080/booking/period?start="+start+" 00:00:00&end="+end+" 23:59:59").done(function(data, success){
        $.each(data, function(key, value) {
            var start = new Date(value.date);
            var end = new Date(start).setHours(start.getHours() + 1);
            cal.createSchedules([{
              id: String(chance.guid()),
              calendarId: calendar.id,
                title: "Slot already booked",
                isAllDay: false,
                start: start,
                end: end,
                category: 'time',
                dueDateClass: '',
                color: "white",
                bgColor: "red",
                isReadOnly: true,
                dragBgColor: calendar.bgColor,
                borderColor: calendar.borderColor,
                raw: {
                    location: location
                },
                state: 'Busy'
            }]);
          });
        }).fail(console.log("failed."));
    }

      function onChangeNewScheduleCalendar(e) {
          var target = $(e.target).closest('a[role="menuitem"]')[0];
          var calendarId = getDataAction(target);
          changeNewScheduleCalendar(calendarId);
      }
      function changeNewScheduleCalendar(calendarId) {
          var calendarNameElement = document.getElementById('calendarName');
          var calendar = findCalendar(calendarId);
          var html = [];
          html.push('<span class="calendar-bar" style="background-color: ' + calendar.bgColor + '; border-color:' + calendar.borderColor + ';"></span>');
          html.push('<span class="calendar-name">' + calendar.name + '</span>');
          calendarNameElement.innerHTML = html.join('');
          selectedCalendar = calendar;
      }
      function createNewSchedule(event) {
          var start = event.start ? new Date(event.start.getTime()) : new Date();
          var end = event.end ? new Date(event.end.getTime()) : moment().add(1, 'hours').toDate();
            cal.openCreationPopup({
                subject: "Booking",
                start: start,
                end: end
            });
      }
      function saveNewSchedule(scheduleData) {
          var start = scheduleData.start;
          var calendar = scheduleData.calendar || findCalendar(scheduleData.calendarId);
          if (guid != ''){
            var lastEvent = $("div[data-schedule-id="+guid+"]");
            cal.deleteSchedule(guid, "");
            while (ScheduleList.length > 0) {
                    ScheduleList.pop();
                }
          }
          var end = new Date(start).setHours(start.getHours() + 1);
          var schedule = {
              id: String(chance.guid()),
              title: "New booking",
              isAllDay: false,
              start: start,
              end: end,
              category: scheduleData.isAllDay ? 'allday' : 'time',
              dueDateClass: '',
              color: "black",
              bgColor: "yellow"
          };
          if (calendar) {
              schedule.calendarId = calendar.id;
              schedule.borderColor = calendar.borderColor;
          }
          ScheduleList.push(schedule);
          cal.createSchedules([schedule]);
          refreshScheduleVisibility();
          guid = schedule.id;
          $("button#commit").prop('disabled', false);
      }
      function refreshScheduleVisibility() {
          var calendarElements = Array.prototype.slice.call(document.querySelectorAll('#calendarList input'));
          CalendarList.forEach(function(calendar) {
              cal.toggleSchedules(calendar.id, !calendar.checked, false);
          });
          cal.render(true);
          calendarElements.forEach(function(input) {
              var span = input.nextElementSibling;
              span.style.backgroundColor = input.checked ? span.style.borderColor : 'transparent';
          });
      }
      function setRenderRangeText() {
          var renderRange = document.getElementById('renderRange');
          var options = cal.getOptions();
          var viewName = cal.getViewName();
          var html = [];
          if (viewName === 'day') {
              html.push(moment(cal.getDate().getTime()).format('YYYY.MM.DD'));
          } else if (viewName === 'month' &&
              (!options.month.visibleWeeksCount || options.month.visibleWeeksCount > 4)) {
              html.push(moment(cal.getDate().getTime()).format('YYYY.MM'));
          } else {
              html.push(moment(cal.getDateRangeStart().getTime()).format('YYYY.MM.DD'));
              html.push(' ~ ');
              html.push(moment(cal.getDateRangeEnd().getTime()).format(' MM.DD'));
          }
          renderRange.innerHTML = html.join('');
      }
      function setSchedules() {
          cal.clear();
          cal.createSchedules(ScheduleList);
          refreshScheduleVisibility();
      }
      function setEventListener() {
          $('#menu-navi').on('click', onClickNavi);
          $('#btn-new-schedule').on('click', createNewSchedule);
          $('#dropdownMenu-calendars-list').on('click', onChangeNewScheduleCalendar);
          window.addEventListener('resize', resizeThrottled);
      }
      function getDataAction(target) {
          return target.dataset ? target.dataset.action : target.getAttribute('data-action');
      }
      window.cal = cal;
      setRenderRangeText();
      setSchedules();
      setEventListener();
      fetchSchedules();
    $("button#commit").on('click', function(){
        var start = ScheduleList[0].start._date;
        console.log(start.toISOString());
        var customer = $("input#customer").val();
         $.post("http://localhost:8080/booking/new?customer="+customer+"&date="+start.toISOString()).done(function(data, success){
            console.log("added");
            window.location.href = "/confirmation"
            });
    });
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
