import Box from '@mui/material/Box';
import * as React from 'react';

export interface CodeAreaProps {
  errorText: string;
  highlights: Array<{
    row_idx: number;
    col_idxes: {
      start: number;
      end: number;
    };
  }>;
}

export default function CodeArea({ errorText, highlights }: CodeAreaProps) {
  const highlight = function (v: string, i: number): JSX.Element[] {
    if (highlights.some((v) => v.row_idx === i + 1)) {
      return highlights
        .filter((vf) => vf.row_idx === i + 1)
        .map((vm) => (
          <>
            <span>{v.slice(0, vm.col_idxes.start - 1)}</span>
            <span style={{ backgroundColor: 'lemonchiffon' }}>
              {v.slice(vm.col_idxes.start - 1, vm.col_idxes.end - 1)}
            </span>
            <span>{v.slice(vm.col_idxes.end - 1)}</span>
          </>
        ));
    } else {
      return [<span key={0}>{v}</span>];
    }
  };

  return (
    <Box>
      {errorText.length > 0 && (
        <div
          style={{
            width: '100%',
            margin: '8px',
            padding: 0,
            paddingTop: 4,
            paddingBottom: 4,
            borderStyle: 'solid',
            borderWidth: 1,
            borderColor: 'rgba(0, 0, 0, 0.23)',
            borderRadius: 4,
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
              {errorText.split('\n').map((v, i) => (
                <tr
                  key={i + 1}
                  style={{
                    padding: 0,
                  }}
                >
                  <td
                    style={{
                      width: 40,
                      padding: 0,
                      paddingLeft: 8,
                      paddingRight: 8,
                      textAlign: 'right',
                      verticalAlign: 'top',
                      userSelect: 'none',
                      color: 'dimgray',
                    }}
                  >
                    {i + 1}
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
                    {highlight(v, i)}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </Box>
  );
}
