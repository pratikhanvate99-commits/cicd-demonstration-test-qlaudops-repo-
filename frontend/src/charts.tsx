import { Area, AreaChart, CartesianGrid, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'

const deployments = [{ day: 'Mon', count: 12 }, { day: 'Tue', count: 18 }, { day: 'Wed', count: 14 }, { day: 'Thu', count: 23 }, { day: 'Fri', count: 19 }, { day: 'Sat', count: 8 }, { day: 'Sun', count: 16 }]
const utilization = [{ time: '09:00', cpu: 34, memory: 52 }, { time: '10:00', cpu: 48, memory: 57 }, { time: '11:00', cpu: 41, memory: 54 }, { time: '12:00', cpu: 66, memory: 63 }, { time: '13:00', cpu: 52, memory: 59 }, { time: '14:00', cpu: 72, memory: 68 }, { time: '15:00', cpu: 58, memory: 62 }]
const tooltipStyle = { background: '#111b29', border: '1px solid #27364a', borderRadius: 8, color: '#eaf0f8' }

export function DeploymentChart() {
  return <ResponsiveContainer width="100%" height="100%"><AreaChart data={deployments} margin={{ top: 12, right: 5, left: -21, bottom: 0 }}><defs><linearGradient id="deployFill" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stopColor="#42a5ff" stopOpacity={0.25}/><stop offset="100%" stopColor="#42a5ff" stopOpacity={0}/></linearGradient></defs><CartesianGrid stroke="#1b2635" vertical={false}/><XAxis dataKey="day" axisLine={false} tickLine={false} tick={{ fill: '#78879a', fontSize: 11 }}/><YAxis axisLine={false} tickLine={false} tick={{ fill: '#78879a', fontSize: 10 }}/><Tooltip contentStyle={tooltipStyle}/><Area type="monotone" dataKey="count" stroke="#58b2ff" strokeWidth={2} fill="url(#deployFill)"/></AreaChart></ResponsiveContainer>
}

export function ResourceChart() {
  return <ResponsiveContainer width="100%" height="100%"><LineChart data={utilization} margin={{ top: 15, right: 9, left: -24, bottom: 0 }}><CartesianGrid stroke="#1b2635" vertical={false}/><XAxis dataKey="time" axisLine={false} tickLine={false} tick={{ fill: '#78879a', fontSize: 10 }}/><YAxis axisLine={false} tickLine={false} tick={{ fill: '#78879a', fontSize: 10 }} tickFormatter={value => `${value}%`}/><Tooltip contentStyle={tooltipStyle}/><Line type="monotone" dataKey="cpu" stroke="#7e8dff" strokeWidth={2} dot={false}/><Line type="monotone" dataKey="memory" stroke="#2bd4b3" strokeWidth={2} dot={false}/></LineChart></ResponsiveContainer>
}
