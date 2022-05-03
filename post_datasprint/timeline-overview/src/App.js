import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { range } from 'lodash';
import { scaleLinear } from 'd3-scale';
import { csvParse } from 'd3-dsv';
import { extent } from 'd3-array';
import { Tooltip } from "react-svg-tooltip";
import './App.css';

const COLUMN_HEIGHT = 200;
const WIDTH = 800;

const sources = {
  'chrono_quali': {
    url: 'https://docs.google.com/spreadsheets/d/e/2PACX-1vS_IHaGQWmEZoToPx4oql78l9Ac-cnvKxDyJoBym9UjzNXQFKrRhThRw912zIAiXOy3yT52mb0XfNqu/pub?output=csv',
    yearField: 'Year',
    endYearField: 'End Year',
    labelField: 'Headline',
    type: 'qualitative'
  },
  'depenses_militaires': {
    url: 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQJEELzcdsyrFDzrfBGQ1c0beEbL9Bdsk6YX4VPKPCa-w9IUMC1zwwexXW6UI3Z-Q/pub?output=csv',
    yearField: 'Année',
    type: 'quantitative',
    yFields: ['Dépenses en l-t'],

  },
  'budget_dunkerque': {
    url: 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQmd4hLWgCWE_7QSDAPq1G4C3ShRw-d53EoNnRSzX4je2fk-4SQlaC0cGIL1MNprQ/pub?output=csv',
    yearField: 'Années comptables',
    // yFields: ['Soldes comptables', 'Recettes', 'Dépenses'],
    yFields: ['Recettes'],
    type: 'quantitative',
  },
  'pilotage': {
    url: 'https://docs.google.com/spreadsheets/d/e/2PACX-1vTbrSp3ypj9rMXEbz3H3-yCTMwP9rFO9O5DfpbMYXuwQMBxGuST-opqsdnKjO9hTVtN7s3Md2lV1TtL/pub?gid=507416536&single=true&output=csv',
    yearField: 'year',
    type: 'quantitative',
    yFields: ['Nb Sorties pilotage 7Z', 'Nb Entrées pilotage 7Z']
  },
  'pilotage_nb_g5': {
    url: 'https://docs.google.com/spreadsheets/d/e/2PACX-1vTbrSp3ypj9rMXEbz3H3-yCTMwP9rFO9O5DfpbMYXuwQMBxGuST-opqsdnKjO9hTVtN7s3Md2lV1TtL/pub?gid=507416536&single=true&output=csv',
    yearField: 'year',
    type: 'quantitative',
    yFields: [ 'Nb Total G5']
  },
}

function App() {

  const [data, setData] = useState(null);

  useEffect(() => {

    Object.entries(sources)
      .reduce((cur, [source, { url, ...props }]) => {
        return cur.then((res) => {
          return new Promise((resolve) => {
            axios.get(url)
              .then(({ data }) => {
                return resolve({
                  ...res,
                  [source]: {
                    ...props,
                    data: csvParse(data)
                  }
                })
              })
          })

        })
      }, Promise.resolve({}))
      .then((results) => {
        setData(results)
      })
  }, [])
  const decades = range(1700, 1810, 10);
  const margins = {
    top: 10,
    bottom: 10,
    left: 20,
    right: 100
  }
  const xScale = scaleLinear().domain([1700, 1800]).range([margins.left, WIDTH - margins.left - margins.right]);

  return data ? (
    <div className="App">
      <svg width={WIDTH} height={COLUMN_HEIGHT * Object.keys(data).length}>
        <g className="decades">
          {
            decades.map(decade => {
              const x = xScale(decade);
              return (
                <g transform={`translate(${x}, 0)`}>
                  <text x={0} y={15}>
                    {decade}
                  </text>
                  <line
                    stroke="lightgrey"
                    strokeDasharray={4}
                    x1={0}
                    x2={0}
                    y1={0}
                    y2={COLUMN_HEIGHT * Object.keys(data).length}
                  />
                  <text x={0} y={COLUMN_HEIGHT * Object.keys(data).length - 2}>
                    {decade}
                  </text>
                </g>
              )
            })
          }
        </g>
        {
          Object.entries(data)
            .map(([sourceName, { yearField, endYearField, labelField, type, data: dati, yFields }], index) => {

              const colors = ['#215C91', '#916113', '#E0B97A', '#6EBAFF', '#4998DE']
              if (type === 'qualitative') {

                return (
                  <g key={index} style={{ opacity: .5 }}>
                    {
                      dati.filter(d => d[yearField] && d[endYearField])
                        .map((datum, datumIndex) => {
                          const startYear = xScale(+datum[yearField]);
                          const endYear = xScale(+datum[endYearField]);
                          const evtRef = React.createRef();
                          const label = datum[labelField];
                          let color = 'orange';
                          if (label.toLowerCase().includes('guerre')) {
                            color = 'red';
                          }

                          return (
                            <>
                              <rect
                                key={datumIndex}
                                x={startYear}
                                width={endYear - startYear}
                                y={margins.top + 10}
                                height={COLUMN_HEIGHT * Object.keys(data).length - margins.top - margins.bottom - 10}
                                fill={color}
                                ref={evtRef}
                              />
                              <Tooltip triggerRef={evtRef}>
                                <foreignObject x="20" y="20" width="160" height="160">
                                  <div xmlns="http://www.w3.org/1999/xhtml"
                                    style={{
                                      background: 'black',
                                      color: 'white',
                                      padding: '.5rem',
                                    }}
                                  >
                                    {label}
                                  </div>
                                </foreignObject>
                              </Tooltip>
                            </>
                          )
                        })
                    }
                    {
                      dati.filter(d => d[endYearField] === '')
                        .map((datum, datumIndex) => {
                          const startYear = xScale(+datum[yearField]);
                          const label = datum[labelField];
                          let color = 'orange';
                          if (label.toLowerCase().includes('guerre')) {
                            color = 'red';
                          }
                          
                          const evtRef = React.createRef();
                          return (
                            <>
                              <line
                                key={datumIndex}
                                x1={startYear}
                                x2={startYear}
                                y1={margins.top + 10}
                                y2={COLUMN_HEIGHT * Object.keys(data).length - margins.top - margins.bottom - 10}
                                stroke={color}
                                ref={evtRef}
                              />
                              <Tooltip triggerRef={evtRef}>
                                <foreignObject x="20" y="20" width="160" height="160">
                                  <div xmlns="http://www.w3.org/1999/xhtml"
                                    style={{
                                      background: 'black',
                                      color: 'white',
                                      padding: '.5rem',
                                    }}
                                  >
                                    {label}
                                  </div>
                                </foreignObject>
                              </Tooltip>
                            </>
                          )
                        })
                    }
                  </g>
                )
              }
              else {
                const scales = yFields.reduce((s, field) => {
                  return {
                    ...s,
                    [field]: scaleLinear()
                      .domain(extent(dati.filter(datum => +datum[yearField] !== 1793).map(datum => +datum[field].replace(/(\s)/g, ''))))
                      .range([COLUMN_HEIGHT - margins.bottom - margins.top, margins.bottom])

                  }
                }, {})
                return (
                  <g key={index} transform={`translate(0, ${COLUMN_HEIGHT * index})`}>
                    <text>{sourceName}</text>
                    <g className="fields">
                      {
                        yFields
                          .map((yField, yFieldIndex) => {
                            const color = colors[yFieldIndex];
                            return (
                              <g key={yField}>
                                {
                                  dati.map((datum, datumIndex) => {
                                    const next = datumIndex < dati.length - 1 ? dati[datumIndex + 1] : undefined;
                                    const circleRef = React.createRef();
                                    if (+datum[yField].replace(/(\s)/g, '') === 0) {
                                      return null;
                                    }
                                    if (+datum[yearField] === 1793) {
                                      return  null;
                                    }
                                    return (
                                      <>
                                        <circle
                                          cx={xScale(+datum[yearField])}
                                          cy={scales[yField](+datum[yField].replace(/(\s)/g, ''))}
                                          r={2}
                                          fill={color}
                                          ref={circleRef}
                                        />
                                        <Tooltip triggerRef={circleRef}>
                                          <foreignObject x="20" y="20" width="160" height="160">
                                            <div xmlns="http://www.w3.org/1999/xhtml"
                                              style={{
                                                background: 'black',
                                                color: 'white',
                                                padding: '.5rem',
                                              }}
                                            >
                                              {datum[yearField]} : {datum[yField]}
                                            </div>
                                          </foreignObject>
                                        </Tooltip>
                                        {
                                          next && +next[yearField] === +datum[yearField] + 1 && +next[yField] !== 0 ?
                                            <line
                                              stroke={color}
                                              x1={xScale(+datum[yearField])}
                                              x2={xScale(+next[yearField])}
                                              y1={scales[yField](+datum[yField].replace(/(\s)/g, ''))}
                                              y2={scales[yField](+next[yField].replace(/(\s)/g, ''))}
                                            />
                                            : null
                                        }
                                      </>
                                    )
                                  })
                                }
                              </g>
                            )
                          })

                      }
                    </g>
                    <g className="legend">
                      {
                        yFields
                          .map((yField, yFieldIndex) => {
                            const color = colors[yFieldIndex]
                            return (
                              <text
                                x={WIDTH}
                                textAnchor={'end'}
                                y={yFieldIndex * 20 + 20}
                                fill={color}
                                width={margins.right}
                              >
                                {yField}
                              </text>

                            )
                          })
                      }
                    </g>
                    <line
                      x1={0}
                      x2={WIDTH}
                      y1={COLUMN_HEIGHT - margins.bottom - margins.top}
                      y2={COLUMN_HEIGHT - margins.bottom - margins.top}
                      stroke="grey"
                    />
                  </g>
                )
              }
            })
        }
      </svg>
    </div>
  ) : <div>Chargement</div>;
}

export default App;
