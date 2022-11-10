import { Box } from '@mui/material';
import * as React from 'react';

export interface CodeAreaProps {
  errorText: string;
  highlights: Array<{
    row_idx: number;
    col_idxes: {
      start: number;
      end: number;
    };
    text: string;
    type: number;
  }>;
}

export default function CodeArea({ errorText, highlights }: CodeAreaProps) {
  const highlight = function (v: string, i: number): JSX.Element[] {
    if (highlights.some((v) => v.row_idx === i + 1)) {
      let current_highlights = highlights.filter((vf) => vf.row_idx === i + 1);
      if (current_highlights.some((v) => v.type === 1)) {
        // ERROR_MESSAGE（重要なエラー行）があればそれだけを強調表示する
        current_highlights = current_highlights.filter((v) => v.type === 1);
      }

      let jsxElements = [];
      jsxElements.push(
        <span>{v.slice(0, current_highlights[0].col_idxes.start)}</span>,
      );
      current_highlights
        .sort((vf) => vf.col_idxes.start)
        .reduce((pre, cur) => {
          jsxElements.push(
            <>
              <span
                style={{
                  backgroundColor: pre.type === 1 ? '#F5B7B1' : '#F9E79F',
                }}
              >
                {v.slice(pre.col_idxes.start, pre.col_idxes.end)}
              </span>
              <span>{v.slice(pre.col_idxes.end, cur.col_idxes.start)}</span>
            </>,
          );
          return cur;
        });
      const lastHighlight = current_highlights[current_highlights.length - 1];
      jsxElements.push(
        <>
          <span
            style={{
              backgroundColor: lastHighlight.type === 1 ? '#F5B7B1' : '#F9E79F',
            }}
          >
            {v.slice(
              lastHighlight.col_idxes.start,
              lastHighlight.col_idxes.end,
            )}
          </span>
          <span>{v.slice(lastHighlight.col_idxes.end)}</span>
        </>,
      );
      return jsxElements;
    } else {
      return [<span key={0}>{v}</span>];
    }
  };

  const tabelRow = function (i: number, v: JSX.Element[] | string) {
    return (
      <tr
        key={i}
        style={{
          padding: 0,
        }}
      >
        <td
          style={{
            width: 52,
            padding: 0,
            paddingLeft: 8,
            paddingRight: 8,
            textAlign: 'right',
            verticalAlign: 'top',
            userSelect: 'none',
            color: 'dimgray',
            backgroundColor: '#f5f5f5',
          }}
        >
          {i}
        </td>
        <td
          style={{
            padding: 0,
            paddingLeft: 8,
            paddingRight: 8,
            textAlign: 'left',
            verticalAlign: 'top',
            whiteSpace: 'pre-wrap',
          }}
        >
          {v}
        </td>
      </tr>
    );
  };

  return (
    <Box>
      <div
        style={{
          width: '100%',
          padding: '4px',
          borderStyle: 'solid',
          borderWidth: 1,
          borderColor: 'rgba(0, 0, 0, 0.23)',
          borderRadius: 4,
          backgroundColor: '#FFFFFF',
        }}
      >
        <table
          style={{
            width: '100%',
            borderSpacing: 0,
            borderCollapse: 'collapse',
            fontSize: `0.9rem`,
            tableLayout: 'fixed',
          }}
        >
          <tbody>
            {errorText
              .split('\n')
              .map((v, i) => tabelRow(i + 1, highlight(v, i)))}
          </tbody>
        </table>
      </div>
    </Box>
  );
}
