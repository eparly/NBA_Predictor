import React from 'react'
import DatePicker from 'react-datepicker'
import 'react-datepicker/dist/react-datepicker.css'
import './DateNavigator.css'

interface DateNavigatorProps {
    selectedDate: Date
    onDateChange: (date: Date) => void
}

const DateNavigator: React.FC<DateNavigatorProps> = ({
    selectedDate, onDateChange
}) => {
    const handlePreviousDay = () => {
        const previousDay = new Date(selectedDate)
        previousDay.setDate(previousDay.getDate() - 1)
        onDateChange(previousDay)
    }

    const handleNextDay = () => {
        const nextDay = new Date(selectedDate)
        nextDay.setDate(nextDay.getDate() + 1)
        onDateChange(nextDay)
    }

    return (
        <div className="date-navigator-container">
            <button className='nav-button' onClick={handlePreviousDay}>Previous Day</button>
            <DatePicker
                selected={selectedDate}
                onChange={(date: Date | null) => {
                    if (date) onDateChange(date)
                }}
                dateFormat={"yyyy-MM-dd"}
                maxDate={new Date()}
                className="custom-date-picker"
                calendarClassName='custom-calendar'
            />
            <button className='nav-button' onClick={handleNextDay}>Next Day</button>
        </div>
    )
}

export default DateNavigator