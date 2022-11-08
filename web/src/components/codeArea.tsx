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
      return highlights
        .filter((vf) => vf.row_idx === i + 1)
        .map((vm) => (
          <>
            <span>{v.slice(0, vm.col_idxes.start)}</span>
            <span
              style={{ backgroundColor: vm.type === 1 ? '#F5B7B1' : '#F9E79F' }}
            >
              {v.slice(vm.col_idxes.start, vm.col_idxes.end)}
            </span>
            <span>{v.slice(vm.col_idxes.end)}</span>
          </>
        ));
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
            fontFamily: 'monospace',
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
